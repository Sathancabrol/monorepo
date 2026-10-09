"""Discord application-command interface for LAPLACE (no message-content intent)."""

from __future__ import annotations

import io
import logging

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .agent import LaplaceAgent
from .config import Settings
from .llm import LLMError
from .memory import MemoryStore, export_json
from .persona import AGENT_NAME

logger = logging.getLogger(__name__)
DISCORD_TEXT_LIMIT = 1900
MAX_IMAGE_BYTES = 8 * 1024 * 1024


def detect_image_mime_type(image_data: bytes) -> str | None:
    """Accept only common static image formats and verify their file signatures."""
    if image_data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image_data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if len(image_data) >= 12 and image_data[:4] == b"RIFF" and image_data[8:12] == b"WEBP":
        return "image/webp"
    return None


def interaction_is_allowed(
    *,
    guild_id: int | None,
    channel_id: int | None,
    allowed_guild_ids: frozenset[int],
    allowed_channel_ids: frozenset[int],
) -> bool:
    """Only allow configured guilds and (when supplied) configured channels."""
    if guild_id is None or guild_id not in allowed_guild_ids:
        return False
    return not allowed_channel_ids or channel_id in allowed_channel_ids


def split_discord_text(text: str, limit: int = DISCORD_TEXT_LIMIT) -> list[str]:
    """Split responses below Discord's 2,000-character content limit."""
    text = text.strip() or "(réponse vide)"
    chunks: list[str] = []
    while len(text) > limit:
        split_at = text.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = text.rfind(" ", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(text[:split_at].rstrip())
        text = text[split_at:].lstrip()
    if text:
        chunks.append(text)
    return chunks


class LaplaceBot(commands.Bot):
    def __init__(
        self,
        settings: Settings,
        store: MemoryStore,
        agent: LaplaceAgent,
    ) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.settings = settings
        self.store = store
        self.agent = agent
        self._register_commands()

    async def setup_hook(self) -> None:
        await self.store.initialize()
        removed = await self.store.purge_expired(self.settings.archive_retention_days)
        if removed:
            logger.info("Retention cleanup removed %s archived interaction(s).", removed)

        # Guild-scoped sync prevents accidental publication outside Olympus.
        for guild_id in sorted(self.settings.allowed_guild_ids):
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        if not self.retention_cleanup.is_running():
            self.retention_cleanup.start()

    @tasks.loop(hours=1)
    async def retention_cleanup(self) -> None:
        try:
            removed = await self.store.purge_expired(self.settings.archive_retention_days)
            if removed:
                logger.info("Retention cleanup removed %s archived interaction(s).", removed)
        except Exception:
            logger.exception("Retention cleanup failed; user content omitted from logs.")

    @retention_cleanup.before_loop
    async def wait_for_gateway_before_cleanup(self) -> None:
        await self.wait_until_ready()

    async def close(self) -> None:
        if self.retention_cleanup.is_running():
            self.retention_cleanup.cancel()
        for provider in (self.agent.provider, self.agent.vision_provider):
            if provider is None:
                continue
            close = getattr(provider, "close", None)
            if close is not None:
                try:
                    await close()
                except Exception:
                    logger.debug("Provider close hook was unavailable.")
        await self.store.close()
        await super().close()

    def _allowed(self, interaction: discord.Interaction) -> bool:
        return interaction_is_allowed(
            guild_id=interaction.guild_id,
            channel_id=interaction.channel_id,
            allowed_guild_ids=self.settings.allowed_guild_ids,
            allowed_channel_ids=self.settings.allowed_channel_ids,
        )

    async def _deny(self, interaction: discord.Interaction) -> None:
        message = "LAPLACE n'est pas activé dans ce serveur ou ce salon."
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    async def _private_message(self, interaction: discord.Interaction, content: str) -> None:
        chunks = split_discord_text(content)
        allowed_mentions = discord.AllowedMentions.none()
        if interaction.response.is_done():
            await interaction.followup.send(
                chunks[0], ephemeral=True, allowed_mentions=allowed_mentions
            )
        else:
            await interaction.response.send_message(
                chunks[0], ephemeral=True, allowed_mentions=allowed_mentions
            )
        for chunk in chunks[1:]:
            await interaction.followup.send(
                chunk, ephemeral=True, allowed_mentions=allowed_mentions
            )

    def _register_commands(self) -> None:
        @self.tree.command(name="parler", description="Discuter avec LAPLACE.")
        async def parler(interaction: discord.Interaction, question: str) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            if not question.strip() or len(question) > 4000:
                await self._private_message(
                    interaction, "La question doit faire entre 1 et 4000 caractères."
                )
                return
            await interaction.response.defer(
                ephemeral=self.settings.private_responses,
                thinking=True,
            )
            try:
                answer = await self.agent.answer(
                    user_id=interaction.user.id,
                    guild_id=interaction.guild_id or 0,
                    channel_id=interaction.channel_id or 0,
                    interaction_id=interaction.id,
                    question=question.strip(),
                )
            except LLMError:
                await interaction.followup.send(
                    "Je n'arrive pas à joindre le modèle. Vérifie qu'Ollama "
                    "(ou le fournisseur API) est démarré et que le modèle "
                    "configuré est disponible.",
                    ephemeral=self.settings.private_responses,
                )
                return
            except Exception:
                logger.exception("LAPLACE request failed; message content omitted from logs.")
                await interaction.followup.send(
                    "La demande a échoué. Aucun détail privé n'a été ajouté aux journaux.",
                    ephemeral=self.settings.private_responses,
                )
                return

            for chunk in split_discord_text(answer):
                await interaction.followup.send(
                    chunk,
                    ephemeral=self.settings.private_responses,
                    allowed_mentions=discord.AllowedMentions.none(),
                )

        @self.tree.command(
            name="aide", description="Afficher les commandes et les règles de confidentialité."
        )
        async def aide(interaction: discord.Interaction) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            text = (
                "**LAPLACE — commandes disponibles**\n"
                "• `/parler question` — discuter avec l'assistant.\n"
                "• `/analyser_image image question` — analyser l'image jointe sans la mémoriser.\n"
                "• `/retenir contenu portee` — mémoriser volontairement un fait privé ou partagé.\n"
                "• `/souvenirs recherche` — consulter/rechercher tes souvenirs "
                "et les souvenirs partagés.\n"
                "• `/corriger id contenu` — corriger un souvenir en gardant sa trace de révision.\n"
                "• `/oublier id` — supprimer un souvenir que tu peux gérer.\n"
                "• `/historique recherche` — rechercher dans ton archive de conversations.\n"
                "• `/exporter_mes_donnees` — exporter tes souvenirs et conversations archivées.\n"
                "• `/effacer_mes_donnees confirmer` — supprimer tes souvenirs privés "
                "et ton archive.\n"
                "• `/statut` — voir le modèle et les réglages non sensibles.\n\n"
                "Les réponses sont privées par défaut. Les conversations traitées par `/parler` "
                "sont archivées pour la durée configurée; chaque personne a un espace séparé. "
                "Les souvenirs partagés sont visibles uniquement dans le serveur "
                "où ils ont été créés. Seuls les propriétaires configurés peuvent "
                "les créer, modifier ou supprimer. Cette version ne lit pas les "
                "messages ordinaires et ne contrôle pas le PC."
            )
            await self._private_message(interaction, text)

        @self.tree.command(
            name="statut", description="Vérifier le statut de LAPLACE sans révéler de secret."
        )
        async def statut(interaction: discord.Interaction) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            provider = (
                "Ollama local"
                if self.settings.llm_provider == "ollama"
                else "API compatible OpenAI"
            )
            archive = (
                f"{self.settings.archive_retention_days} jour(s)"
                if self.settings.archive_retention_days
                else "désactivée"
            )
            visibility = "privées" if self.settings.private_responses else "publiques dans le salon"
            vision = (
                f"{self.settings.vision_provider} / `{self.settings.vision_model}`"
                if self.settings.vision_model
                else "désactivée"
            )
            message = (
                f"**{AGENT_NAME}** est connecté.\n"
                f"• Fournisseur : {provider}\n"
                f"• Modèle : `{self.settings.llm_model}`\n"
                f"• Analyse d’image : {vision}\n"
                f"• Réponses : {visibility}\n"
                f"• Archive brute : {archive}\n"
                f"• Historique transmis au modèle : {self.settings.max_history_turns} "
                "échange(s) au maximum\n"
                "Aucun jeton ni aucune clé API n'est affiché."
            )
            await self._private_message(interaction, message)

        @self.tree.command(
            name="analyser_image",
            description="Analyser une image jointe sans l'ajouter à la mémoire.",
        )
        async def analyser_image(
            interaction: discord.Interaction,
            image: discord.Attachment,
            question: str,
        ) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            if self.agent.vision_provider is None:
                await self._private_message(
                    interaction,
                    "L'analyse d'image est désactivée. Configure un modèle compatible dans "
                    "VISION_MODEL; une API externe exige ALLOW_EXTERNAL_VISION=true.",
                )
                return
            if not question.strip() or len(question) > 1000:
                await self._private_message(
                    interaction, "La question d'analyse doit faire entre 1 et 1000 caractères."
                )
                return
            if image.size > MAX_IMAGE_BYTES:
                await self._private_message(
                    interaction, "L'image dépasse la limite de 8 Mio pour cette version."
                )
                return

            await interaction.response.defer(ephemeral=True, thinking=True)
            try:
                image_data = await image.read()
            except discord.HTTPException:
                await self._private_message(
                    interaction, "L'image n'a pas pu être récupérée depuis Discord."
                )
                return
            if len(image_data) > MAX_IMAGE_BYTES:
                await self._private_message(
                    interaction, "L'image dépasse la limite de 8 Mio pour cette version."
                )
                return
            mime_type = detect_image_mime_type(image_data)
            if mime_type is None:
                await self._private_message(
                    interaction, "Formats acceptés : images JPEG, PNG ou WebP valides."
                )
                return

            try:
                answer = await self.agent.analyze_image(
                    image_data=image_data,
                    mime_type=mime_type,
                    question=question.strip(),
                )
            except LLMError:
                await self._private_message(
                    interaction,
                    "Le modèle vision n'a pas répondu ou ne prend pas en charge les images. "
                    "Vérifie VISION_MODEL et les capacités du modèle configuré.",
                )
                return
            except Exception:
                logger.exception("Image analysis failed; attachment content omitted from logs.")
                await self._private_message(
                    interaction,
                    "L'analyse a échoué. L'image n'a pas été ajoutée à la mémoire.",
                )
                return
            await self._private_message(interaction, answer)

        @self.tree.command(name="retenir", description="Ajouter un souvenir avec provenance.")
        @app_commands.choices(
            portee=[
                app_commands.Choice(name="Privée — visible uniquement par moi", value="private"),
                app_commands.Choice(
                    name="Partagée — visible dans le serveur courant", value="shared"
                ),
            ]
        )
        async def retenir(
            interaction: discord.Interaction,
            contenu: str,
            portee: app_commands.Choice[str],
            source_url: str | None = None,
            confiance: float = 1.0,
        ) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            scope = portee.value
            if scope == "shared" and interaction.user.id not in self.settings.owner_user_ids:
                await self._private_message(
                    interaction,
                    "Seul un propriétaire de LAPLACE peut ajouter une connaissance partagée. "
                    "Tu peux choisir une mémoire privée.",
                )
                return
            if not 0.0 <= confiance <= 1.0:
                await self._private_message(
                    interaction, "La confiance doit être comprise entre 0 et 1."
                )
                return
            try:
                memory_id = await self.store.add_memory(
                    content=contenu,
                    scope=scope,
                    user_id=interaction.user.id,
                    interaction_id=interaction.id,
                    guild_id=interaction.guild_id or 0,
                    channel_id=interaction.channel_id or 0,
                    confidence=confiance,
                    source_url=source_url,
                )
            except ValueError as exc:
                await self._private_message(interaction, str(exc))
                return
            label = "privé" if scope == "private" else "partagé"
            await self._private_message(
                interaction, f"Souvenir #{memory_id} enregistré en portée **{label}**."
            )

        @self.tree.command(
            name="souvenirs",
            description="Lister ou rechercher tes souvenirs et les souvenirs partagés.",
        )
        async def souvenirs(interaction: discord.Interaction, recherche: str | None = None) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            if recherche and recherche.strip():
                records = await self.store.search_memories(
                    interaction.user.id,
                    recherche.strip(),
                    limit=10,
                    guild_id=interaction.guild_id or 0,
                )
            else:
                records = await self.store.list_memories(
                    interaction.user.id,
                    guild_id=interaction.guild_id or 0,
                    include_shared=True,
                    limit=15,
                )
            if not records:
                await self._private_message(interaction, "Aucun souvenir correspondant.")
                return
            lines = ["**Souvenirs (privés et partagés)**"]
            for record in records:
                scope_label = "privé" if record["scope"] == "private" else "partagé"
                source = record.get("source_url") or "source: commande Discord"
                snippet = str(record["content"]).replace("\n", " ")[:260]
                lines.append(
                    f"• `#{record['id']}` ({scope_label}; confiance {record['confidence']:.2f}; "
                    f"{record['created_at'][:10]}) {snippet}\n  _{source}_"
                )
            await self._private_message(interaction, "\n".join(lines))

        @self.tree.command(
            name="corriger",
            description="Corriger un souvenir sans perdre la trace de la modification.",
        )
        async def corriger(
            interaction: discord.Interaction,
            identifiant: int,
            nouveau_contenu: str,
        ) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            changed = await self.store.correct_memory(
                memory_id=identifiant,
                user_id=interaction.user.id,
                guild_id=interaction.guild_id or 0,
                new_content=nouveau_contenu,
                can_manage_shared=interaction.user.id in self.settings.owner_user_ids,
            )
            message = (
                f"Souvenir #{identifiant} corrigé; l'ancienne version reste "
                "dans l'historique de révision."
                if changed
                else "Souvenir introuvable ou tu n'as pas le droit de le modifier."
            )
            await self._private_message(interaction, message)

        @self.tree.command(
            name="oublier", description="Supprimer un souvenir privé ou partagé que tu peux gérer."
        )
        async def oublier(interaction: discord.Interaction, identifiant: int) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            deleted = await self.store.forget_memory(
                memory_id=identifiant,
                user_id=interaction.user.id,
                guild_id=interaction.guild_id or 0,
                can_manage_shared=interaction.user.id in self.settings.owner_user_ids,
            )
            message = (
                f"Souvenir #{identifiant} supprimé, y compris ses révisions."
                if deleted
                else "Souvenir introuvable ou tu n'as pas le droit de le supprimer."
            )
            await self._private_message(interaction, message)

        @self.tree.command(
            name="historique", description="Rechercher dans ta propre archive de conversations."
        )
        async def historique(interaction: discord.Interaction, recherche: str) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            await self.store.purge_expired(self.settings.archive_retention_days)
            records = await self.store.search_archive(interaction.user.id, recherche, limit=5)
            if not records:
                await self._private_message(
                    interaction,
                    "Aucun échange trouvé (ou l'archive est désactivée/expirée).",
                )
                return
            lines = ["**Extraits de ton archive personnelle**"]
            for record in records:
                date = str(record["created_at"])[:10]
                question = str(record["request"]).replace("\n", " ")[:250]
                answer = str(record["response"]).replace("\n", " ")[:450]
                lines.append(f"• `{date}` — **Toi :** {question}\n  **LAPLACE :** {answer}")
            await self._private_message(interaction, "\n\n".join(lines))

        @self.tree.command(
            name="exporter_mes_donnees",
            description="Télécharger une copie JSON de tes données LAPLACE.",
        )
        async def exporter_mes_donnees(interaction: discord.Interaction) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            await self.store.purge_expired(self.settings.archive_retention_days)
            data = await self.store.export_user_data(interaction.user.id)
            attachment = discord.File(
                io.BytesIO(export_json(data)),
                filename=f"laplace-export-{interaction.user.id}.json",
            )
            await interaction.response.send_message(
                "Voici l'export de tes souvenirs privés, de leurs révisions et de ton archive.",
                file=attachment,
                ephemeral=True,
            )

        @self.tree.command(
            name="effacer_mes_donnees",
            description="Effacer tes souvenirs privés et ton archive. Action irréversible.",
        )
        async def effacer_mes_donnees(
            interaction: discord.Interaction,
            confirmer: bool,
        ) -> None:
            if not self._allowed(interaction):
                await self._deny(interaction)
                return
            if not confirmer:
                await self._private_message(
                    interaction,
                    "Aucune donnée effacée. Relance la commande avec `confirmer: true` pour "
                    "supprimer tes souvenirs privés, révisions et échanges archivés. "
                    "Les connaissances partagées restent intactes.",
                )
                return
            counts = await self.store.forget_all_user_data(interaction.user.id)
            await self._private_message(
                interaction,
                f"Données effacées : {counts['memories']} souvenir(s) privé(s) et "
                f"{counts['interactions']} échange(s) archivé(s). "
                "Les souvenirs partagés n'ont pas été modifiés.",
            )


def build_bot(settings: Settings) -> LaplaceBot:
    store = MemoryStore(settings.database_path)
    from .llm import LLMClient

    provider = LLMClient(settings)
    vision_provider = None
    if settings.vision_model and settings.vision_base_url and settings.vision_api_key:
        vision_provider = LLMClient(
            settings,
            model=settings.vision_model,
            base_url=settings.vision_base_url,
            api_key=settings.vision_api_key,
        )
    agent = LaplaceAgent(
        provider,
        store,
        vision_provider=vision_provider,
        history_turns=settings.max_history_turns,
        memory_top_k=settings.memory_top_k,
        archive_retention_days=settings.archive_retention_days,
    )
    return LaplaceBot(settings, store, agent)
