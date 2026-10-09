from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from laplace.memory import MemoryStore


@pytest.fixture
async def store(tmp_path):
    db = MemoryStore(tmp_path / "laplace.sqlite3")
    await db.initialize()
    yield db
    await db.close()


async def add_memory(
    store,
    *,
    user_id: int,
    content: str,
    scope: str = "private",
    guild_id: int = 123,
    **kwargs,
) -> int:
    return await store.add_memory(
        content=content,
        scope=scope,
        user_id=user_id,
        interaction_id=1000 + user_id,
        guild_id=guild_id,
        channel_id=456,
        **kwargs,
    )


@pytest.mark.asyncio
async def test_private_memories_and_chat_history_are_isolated_by_user(store) -> None:
    await add_memory(store, user_id=10, content="La couleur préférée est bleu.")
    await add_memory(store, user_id=20, content="La couleur préférée est vert.")
    await store.archive_interaction(
        interaction_id=1,
        user_id=10,
        guild_id=123,
        channel_id=456,
        request="Je préfère le thé",
        response="Je le note.",
    )
    assert (
        "bleu"
        in (await store.search_memories(10, "couleur préférée", 5, guild_id=123))[0]["content"]
    )
    assert await store.search_memories(20, "bleu", 5, guild_id=123) == []
    assert await store.get_recent_turns(20, 5) == []
    assert (await store.get_recent_turns(10, 5))[0]["request"] == "Je préfère le thé"


@pytest.mark.asyncio
async def test_shared_memories_are_retrievable_but_private_memories_are_not(store) -> None:
    await add_memory(
        store, user_id=10, content="Règle partagée du serveur: salon calme", scope="shared"
    )
    await add_memory(store, user_id=10, content="Adresse personnelle", scope="private")
    results = await store.search_memories(20, "salon calme", 5, guild_id=123)
    assert [row["scope"] for row in results] == ["shared"]
    assert await store.search_memories(20, "Adresse personnelle", 5, guild_id=123) == []


@pytest.mark.asyncio
async def test_shared_memories_are_scoped_to_their_guild(store) -> None:
    memory_id = await add_memory(
        store,
        user_id=10,
        content="Annonce réservée au premier serveur",
        scope="shared",
        guild_id=123,
    )
    assert await store.search_memories(20, "premier serveur", 5, guild_id=999) == []
    assert await store.list_memories(20, guild_id=999) == []
    assert not await store.correct_memory(
        memory_id=memory_id,
        user_id=10,
        guild_id=999,
        new_content="Modification depuis un autre serveur",
        can_manage_shared=True,
    )
    assert await store.correct_memory(
        memory_id=memory_id,
        user_id=10,
        guild_id=123,
        new_content="Annonce corrigée dans le bon serveur",
        can_manage_shared=True,
    )


@pytest.mark.asyncio
async def test_memory_correction_preserves_a_revision_and_forget_checks_owner(store) -> None:
    memory_id = await add_memory(
        store,
        user_id=10,
        content="Rendez-vous mardi",
        source_url="https://discord.com/channels/123/456/789",
    )
    assert not await store.correct_memory(
        memory_id=memory_id, user_id=20, guild_id=123, new_content="Rendez-vous jeudi"
    )
    assert await store.correct_memory(
        memory_id=memory_id, user_id=10, guild_id=123, new_content="Rendez-vous jeudi"
    )
    exported = await store.export_user_data(10)
    assert exported["memories"][0]["content"] == "Rendez-vous jeudi"
    assert exported["memory_revisions"][0]["previous_content"] == "Rendez-vous mardi"
    assert not await store.forget_memory(memory_id=memory_id, user_id=20, guild_id=123)
    assert await store.forget_memory(memory_id=memory_id, user_id=10, guild_id=123)
    assert await store.list_memories(10, guild_id=123) == []


@pytest.mark.asyncio
async def test_source_url_must_be_https_and_confidence_is_bounded(store) -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        await add_memory(
            store, user_id=10, content="Source non sûre", source_url="http://example.com"
        )
    with pytest.raises(ValueError, match="confiance"):
        await store.add_memory(
            content="Fait",
            scope="private",
            user_id=10,
            interaction_id=1,
            guild_id=2,
            channel_id=3,
            confidence=1.5,
        )


@pytest.mark.asyncio
async def test_archive_retention_and_explicit_data_erasure(store) -> None:
    old = (datetime.now(UTC) - timedelta(days=40)).isoformat(timespec="seconds")
    await store.archive_interaction(
        interaction_id=1,
        user_id=10,
        guild_id=123,
        channel_id=456,
        request="Ancienne demande",
        response="Ancienne réponse",
        created_at=old,
    )
    await store.archive_interaction(
        interaction_id=2,
        user_id=20,
        guild_id=123,
        channel_id=456,
        request="Autre personne",
        response="Ne pas supprimer",
    )
    assert await store.purge_expired(30) == 1
    assert await store.get_recent_turns(10, 5) == []
    private_id = await add_memory(store, user_id=10, content="Souvenir privé")
    shared_id = await add_memory(store, user_id=10, content="Fait partagé", scope="shared")
    await store.archive_interaction(
        interaction_id=3,
        user_id=10,
        guild_id=123,
        channel_id=456,
        request="Question",
        response="Réponse",
    )
    result = await store.forget_all_user_data(10)
    assert result["memories"] == 1
    assert result["interactions"] == 1
    remaining = await store.list_memories(10, guild_id=123)
    assert [row["id"] for row in remaining] == [shared_id]
    assert (await store.get_recent_turns(20, 5))[0]["request"] == "Autre personne"
    assert private_id != shared_id


@pytest.mark.asyncio
async def test_zero_retention_purges_archive_but_not_explicit_memories(store) -> None:
    await store.archive_interaction(
        interaction_id=1,
        user_id=10,
        guild_id=123,
        channel_id=456,
        request="Question",
        response="Réponse",
    )
    await add_memory(store, user_id=10, content="Souvenir conservé")
    assert await store.purge_expired(0) == 1
    assert await store.get_recent_turns(10, 5) == []
    assert len(await store.list_memories(10, guild_id=123)) == 1
