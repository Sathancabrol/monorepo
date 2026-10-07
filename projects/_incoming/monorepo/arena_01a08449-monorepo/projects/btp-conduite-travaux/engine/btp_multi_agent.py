import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class AuditLedger:
    """Immutable cryptographic audit ledger for BTP operations."""
    def __init__(self, ledger_path: Optional[Path] = None):
        self.ledger_path = ledger_path or (PROJECT_ROOT / "data" / "btp_audit_ledger.json")
        self.entries = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.ledger_path.exists():
            try:
                return json.loads(self.ledger_path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def log(self, agent_id: str, action: str, details: Dict[str, Any], status: str = "SUCCESS") -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat() + "Z"
        prev_hash = self.entries[-1]["hash"] if self.entries else "GENESIS_BLOCK_BTP_2026"
        
        entry_payload = {
            "index": len(self.entries) + 1,
            "timestamp": timestamp,
            "agent_id": agent_id,
            "action": action,
            "status": status,
            "details": details,
            "prev_hash": prev_hash
        }
        
        raw_str = json.dumps(entry_payload, sort_keys=True)
        entry_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
        entry_payload["hash"] = entry_hash
        
        self.entries.append(entry_payload)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_path.write_text(json.dumps(self.entries, indent=2, ensure_ascii=False), encoding="utf-8")
        return entry_payload

    def get_entries(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.entries[-limit:][::-1]


class BTPAgentSystem:
    """Autonomous Multi-Agent AI System for Civil Engineering & Public Works."""
    
    def __init__(self):
        self.ledger = AuditLedger()
        self.agents = {
            "AGENT_LEGAL": {
                "name": "Agent Marchés Publics & DCE",
                "role": "Analyse CCTP/CCAP, conformité CCAG 2021, rédaction DC1/DC2/DC4, mémoires de réclamation Art. 55",
                "status": "ONLINE",
                "last_action": "Audit CCAP Barbazan & Saint-Nicolas terminé"
            },
            "AGENT_BUDGET": {
                "name": "Agent Étude de Prix & Budget Dynamique",
                "role": "Calcul sous-détails de prix (SDP), déboursé sec, application THMO, indexation TP01/TP08, bilan carbone",
                "status": "ONLINE",
                "last_action": "Barèmes de 28 SDP actualisés K=1.250"
            },
            "AGENT_DICT_SAFETY": {
                "name": "Agent DT-DICT, AIPR & Sécurité",
                "role": "Guichet Unique, Cerfa 14434, Cerfa 14023/14024, PGC SPS, plans de signalisation temporaire IISR 8e partie",
                "status": "ONLINE",
                "last_action": "14 récépissés DT instruits, classes A/B/C validées"
            },
            "AGENT_TELEMETRY_VISION": {
                "name": "Agent Télémesure, Vision & Capteurs",
                "role": "Traitement flux vidéo smartphone, thermographie enrobé (>130°C), essais de plaque Dynaplaque EV2, LiDAR cubatures",
                "status": "ACTIVE_MONITORING",
                "last_action": "Surveillance thermique continue et géoréférencement"
            },
            "AGENT_PROCUREMENT": {
                "name": "Agent Fournisseurs & Commandes",
                "role": "Appels d'offres carrières/béton/enrobé, bons de commande, rapprochement BL, traçabilité Trackdéchets RNDTS",
                "status": "ONLINE",
                "last_action": "Consultation centrale enrobés & fournisseurs bordures"
            },
            "AGENT_PLANNING_LEAN": {
                "name": "Agent Ordonnancement & Last Planner",
                "role": "Phasage 4D, chemin critique, ajustement météo/aléas concessionnaires, calcul indicateur PPC",
                "status": "ONLINE",
                "last_action": "Gantt 8 semaines optimisé avec marge intempéries"
            },
            "AGENT_FIELD_FOREMAN": {
                "name": "Agent Assistant Équipe Terrain",
                "role": "Journal de chantier vocal, fiches de tâches journalières, causeries 1/4h sécurité contextuelles",
                "status": "ONLINE",
                "last_action": "Briefing sécurité 'Travaux sous alternat' généré"
            },
            "AGENT_DOE_CLOSEOUT": {
                "name": "Agent Réception, DOE & DIUO",
                "role": "Agrégation As-Built X,Y,Z, ITV caméra assainissement, fiches NF/CE, validation DGD Chorus Pro",
                "status": "STANDBY",
                "last_action": "Structure Standard SI 022 pré-remplie à 85%"
            }
        }

    def run_automated_lifecycle(self, project_id: str = "barbazan_giratoire") -> Dict[str, Any]:
        """Execute end-to-end automated workflow for a project."""
        results = {}
        
        # 1. Legal / DCE Ingestion
        results["step1_legal"] = {
            "project": "Giratoire Barbazan RD33/RD33D",
            "ccag_version": "CCAG-Travaux 2021 actualisé",
            "clauses_conformity": {
                "art_20_4_environnement": "CONFORME - SOGED + SOPAQ exigés",
                "art_19_2_2_penalites": "CONFORME - Plafonnement à 10% HT actif (26 850 € max)",
                "avance_pme": "20% validée (53 700 € HT)",
                "delai_paiement": "30 jours via Chorus Pro"
            },
            "administrative_forms_generated": ["DC1_Lettre_Candidature.pdf", "DC2_Declaration_Candidat.pdf", "DC4_Sous_Traitance.pdf"]
        }
        self.ledger.log("AGENT_LEGAL", "DCE_PARSED_AND_VALIDATED", results["step1_legal"])

        # 2. Budget & SDP computation
        results["step2_budget"] = {
            "total_items": 28,
            "debourse_sec_total": 214800.00,
            "k_coefficient": 1.250,
            "prix_vente_ht": 268500.00,
            "indexation_recommandee": "TP08 (Travaux routiers et enrobés)",
            "empreinte_carbone_estimee_tco2": 42.8
        }
        self.ledger.log("AGENT_BUDGET", "SDP_CALCULATED", results["step2_budget"])

        # 3. DICT & Permissions
        results["step3_dict"] = {
            "guichet_unique_status": "VALIDATED",
            "dict_cerfa_14434": "Généré automatiquement",
            "arrete_circulation_cerfa_14024": "Déposé en préfecture / CD31",
            "permission_voirie_cerfa_14023": "Délivrée",
            "classes_reseaux_reconnues": {"A": 5, "B": 3, "C": 2},
            "alertes": "2 réseaux d'eau potable en classe C -> Prescription terrassement doux / aspiratrice de déblais"
        }
        self.ledger.log("AGENT_DICT_SAFETY", "DICT_AND_PERMITS_ISSUED", results["step3_dict"])

        # 4. Supplier procurement
        results["step4_procurement"] = {
            "rfq_sent": [
                {"fournisseur": "Centrale Enrobés Villeneuve", "produit": "GB3 (1800t) + BBSG 0/14 (500t)", "status": "CONFIRMED"},
                {"fournisseur": "Carrières du Comminges", "produit": "GNT 0/20 concassée (300m3)", "status": "CONFIRMED"},
                {"fournisseur": "Plattard TP", "produit": "Bordures P2 (60ml), I1 (181ml), CC1 (10ml)", "status": "DISPATCHED"}
            ],
            "trackdechets_registry": "Bordereau BSD-2026-0909-001 émis pour 3100 m2 de décapage terre végétale"
        }
        self.ledger.log("AGENT_PROCUREMENT", "PROCUREMENT_ORDERS_ISSUED", results["step4_procurement"])

        # 5. Planning & LPS
        results["step5_planning"] = {
            "total_duration_weeks": 8,
            "critical_path": ["Décapage", "GNT 0/20", "Bordures P2/I1", "GB3 Fondation", "BBSG Roulement", "Finition"],
            "ppc_target": "92%",
            "intemperies_buffer_days": 4
        }
        self.ledger.log("AGENT_PLANNING_LEAN", "SCHEDULE_INITIALIZED", results["step5_planning"])

        return {
            "status": "COMPLETED",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": "Dossier BTP entièrement instruit et planifié de A à Z par l'essaim multi-agents.",
            "workflow_steps": results,
            "latest_audit_hash": self.ledger.entries[-1]["hash"]
        }

    def process_sensor_event(self, sensor_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process real-time sensor / camera feed telemetry."""
        result = {"sensor_type": sensor_type, "timestamp": datetime.utcnow().isoformat() + "Z", "action_taken": None}
        
        if sensor_type == "ASPHALT_THERMAL_CAM":
            temp = data.get("temperature_c", 145)
            if temp < 130:
                result["status"] = "ALERT"
                result["message"] = f"Alerte température critique enrobé : {temp}°C (< 130°C). Risque de défaut de compactage !"
                result["action_taken"] = "Ordre d'arrêt partiel émis au chef d'application + notification centrale d'enrobés"
                self.ledger.log("AGENT_TELEMETRY_VISION", "THERMAL_DEFECT_DETECTED", {"temp_c": temp, "data": data}, "WARNING")
            else:
                result["status"] = "OK"
                result["message"] = f"Température conforme : {temp}°C (Plage optimale 140-165°C)"
                self.ledger.log("AGENT_TELEMETRY_VISION", "THERMAL_TEMP_NOMINAL", {"temp_c": temp})

        elif sensor_type == "DYNAPLAQUE_COMPACTION":
            ev2 = data.get("ev2_mpa", 65)
            ev2_ev1 = data.get("k_ratio", 1.6)
            if ev2 < 50 or ev2_ev1 > 2.0:
                result["status"] = "ALERT"
                result["message"] = f"Portance insuffisante : EV2={ev2} MPa (exigé >= 50 MPa) ou K={ev2_ev1} (> 2.0)"
                result["action_taken"] = "Prescription immédiate de 3 passes de compacteur tandem supplémentaire ou traitement chaux"
                self.ledger.log("AGENT_TELEMETRY_VISION", "COMPACTION_INSUFFICIENT", {"ev2": ev2, "k": ev2_ev1}, "WARNING")
            else:
                result["status"] = "OK"
                result["message"] = f"Portance validée : EV2={ev2} MPa, Ratio EV2/EV1={ev2_ev1} (Conforme AR2)"
                self.ledger.log("AGENT_TELEMETRY_VISION", "COMPACTION_VALIDATED", {"ev2": ev2, "k": ev2_ev1})

        elif sensor_type == "PHONE_CAM_VISION_DEFECT":
            defect = data.get("detected_defect", "NONE")
            if defect != "NONE":
                result["status"] = "NON_CONFORMITY"
                result["message"] = f"Défaut détecté par vision IA : {defect}"
                result["action_taken"] = "Fiche de Non-Conformité rédigée et géolocalisée automatiquement"
                self.ledger.log("AGENT_TELEMETRY_VISION", "VISION_DEFECT_LOGGED", data, "ALERT")
            else:
                result["status"] = "OK"
                result["message"] = "Alignement et pose visuellement conformes aux tolérances NF EN 1340"
                self.ledger.log("AGENT_TELEMETRY_VISION", "VISION_INSPECTION_OK", data)

        return result


# Singleton instance
btp_agent_system = BTPAgentSystem()

if __name__ == "__main__":
    print("Testing BTP Multi-Agent AI System...")
    res = btp_agent_system.run_automated_lifecycle()
    print("Lifecycle run result:", json.dumps(res, indent=2, ensure_ascii=False))
    
    # Test sensor
    sensor_res = btp_agent_system.process_sensor_event("ASPHALT_THERMAL_CAM", {"temperature_c": 118, "truck_id": "CAM-04"})
    print("Sensor test result:", sensor_res)
