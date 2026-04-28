"""Streamlit frontend for the career guidance AI agent."""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
import streamlit as st

from app.questions import QUESTIONS
from app.recommendations import build_recommendation
from app.scoring import calculate_scores


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="Career Guidance AI Agent", page_icon="CG", layout="wide")

st.title("Career Guidance AI Agent")
st.caption("A counselor-style assessment for engineering students. It asks a full set of questions before recommending a path.")

with st.sidebar:
    st.header("Assessment")
    st.write(f"{len(QUESTIONS)} structured questions")
    use_api = st.toggle("Save results to SQLite through FastAPI", value=True)
    st.divider()
    st.write("Tracks covered:")
    st.write("AI, data, software, cloud, QA, cybersecurity, business analysis, and UI/UX.")


def submit_to_api(student_name: str, answers: dict) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/assess",
        json={"student_name": student_name, "answers": answers},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def local_recommendation(answers: dict) -> dict:
    return {"assessment_id": None, "recommendation": build_recommendation(calculate_scores(answers))}


student_name = st.text_input("Student name", placeholder="Enter your name")

answers = {}
sections = []
for question in QUESTIONS:
    if question["section"] not in sections:
        sections.append(question["section"])

tabs = st.tabs(sections)
for tab, section in zip(tabs, sections):
    with tab:
        for question in [item for item in QUESTIONS if item["section"] == section]:
            if question["type"] == "scale":
                answers[question["id"]] = st.slider(
                    question["text"],
                    min_value=question["min"],
                    max_value=question["max"],
                    value=3,
                    help=f"1 = {question['labels'][1]}, 5 = {question['labels'][5]}",
                )
            elif question["type"] == "choice":
                answers[question["id"]] = st.radio(
                    question["text"],
                    question["options"],
                    horizontal=False,
                )

st.divider()
submitted = st.button("Analyze my career fit", type="primary", use_container_width=True)

if submitted:
    try:
        result = submit_to_api(student_name, answers) if use_api else local_recommendation(answers)
    except Exception as exc:
        st.warning(f"FastAPI was not reachable, so the app generated the recommendation locally. Details: {exc}")
        result = local_recommendation(answers)

    recommendation = result["recommendation"]
    st.success("Assessment complete")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Best-fit track", recommendation["best_fit_career_track"])
    with col2:
        st.metric("Secondary track", recommendation["secondary_track"])

    st.subheader("Reason for recommendation")
    st.write(recommendation["reason"])

    st.subheader("Patterns noticed")
    for pattern in recommendation["patterns"]:
        st.write(f"- {pattern}")

    st.subheader("Skill gaps")
    for gap in recommendation["skill_gaps"]:
        st.write(f"- {gap}")

    st.subheader("3-month learning roadmap")
    for step in recommendation["three_month_learning_roadmap"]:
        st.write(f"- {step}")

    st.subheader("Backup career tracks")
    st.write(", ".join(recommendation["backup_career_tracks"]))

    with st.expander("Score details"):
        sorted_scores = sorted(recommendation["scores"].items(), key=lambda item: item[1], reverse=True)
        st.bar_chart({track: score for track, score in sorted_scores})
