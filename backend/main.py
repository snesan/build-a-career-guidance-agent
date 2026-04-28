"""FastAPI backend for the career guidance AI agent."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.database import init_db, recent_assessments, save_assessment
from app.questions import QUESTIONS, question_count
from app.recommendations import build_recommendation
from app.scoring import calculate_scores


class AssessmentRequest(BaseModel):
    student_name: str = Field(default="Anonymous student")
    answers: dict


app = FastAPI(title="Career Guidance AI Agent")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/questions")
def questions() -> dict:
    return {"count": question_count(), "questions": QUESTIONS}


@app.post("/assess")
def assess(payload: AssessmentRequest) -> dict:
    score_result = calculate_scores(payload.answers)
    recommendation = build_recommendation(score_result)
    assessment_id = save_assessment(payload.student_name, payload.answers, recommendation)
    return {"assessment_id": assessment_id, "recommendation": recommendation}


@app.get("/assessments/recent")
def assessments_recent() -> dict:
    return {"assessments": recent_assessments()}
