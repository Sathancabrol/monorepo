"""Endpoints API pour le Laboratoire d'expérimentations."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.database import get_db_connection
from app.experiment_templates import get_templates

router = APIRouter(prefix="/api", tags=["laboratory"])

class ExperimentCreate(BaseModel):
    name: str
    hypothesis: Optional[str] = None
    iv_name: Optional[str] = None
    iv_levels: Optional[str] = None
    dv_name: Optional[str] = None
    dv_measure: Optional[str] = None
    design: Optional[str] = None
    conditions: Optional[str] = None
    participants: Optional[str] = None
    sample_size: Optional[int] = None
    materials: Optional[str] = None
    procedure: Optional[str] = None
    controls: Optional[str] = None
    ethics: Optional[str] = None
    expected_results: Optional[str] = None
    related_concepts: Optional[str] = None
    analysis_plan: Optional[str] = None
    status: Optional[str] = "draft"

@router.get("/experiments")
def list_experiments():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM experiments ORDER BY updated_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

@router.post("/experiments")
def create_experiment(exp: ExperimentCreate):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO experiments 
        (name,hypothesis,iv_name,iv_levels,dv_name,dv_measure,design,conditions,participants,sample_size,materials,procedure,controls,ethics,expected_results,related_concepts,analysis_plan,status)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (exp.name,exp.hypothesis,exp.iv_name,exp.iv_levels,exp.dv_name,exp.dv_measure,exp.design,exp.conditions,exp.participants,exp.sample_size,exp.materials,exp.procedure,exp.controls,exp.ethics,exp.expected_results,exp.related_concepts,exp.analysis_plan,exp.status))
    conn.commit()
    exp_id = c.lastrowid
    conn.close()
    return {"status":"success","id":exp_id}

@router.put("/experiments/{exp_id}")
def update_experiment(exp_id: int, exp: ExperimentCreate):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""UPDATE experiments SET 
        name=?,hypothesis=?,iv_name=?,iv_levels=?,dv_name=?,dv_measure=?,design=?,conditions=?,participants=?,sample_size=?,materials=?,procedure=?,controls=?,ethics=?,expected_results=?,related_concepts=?,analysis_plan=?,status=?,updated_at=CURRENT_TIMESTAMP
        WHERE id=?""",
        (exp.name,exp.hypothesis,exp.iv_name,exp.iv_levels,exp.dv_name,exp.dv_measure,exp.design,exp.conditions,exp.participants,exp.sample_size,exp.materials,exp.procedure,exp.controls,exp.ethics,exp.expected_results,exp.related_concepts,exp.analysis_plan,exp.status,exp_id))
    conn.commit()
    conn.close()
    return {"status":"success"}

@router.delete("/experiments/{exp_id}")
def delete_experiment(exp_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM experiments WHERE id=?", (exp_id,))
    conn.commit()
    conn.close()
    return {"status":"success"}

@router.get("/experiment-templates")
def get_experiment_templates():
    return get_templates()
