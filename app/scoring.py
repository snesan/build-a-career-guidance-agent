"""Scoring engine that maps counseling answers to career tracks."""

from __future__ import annotations

from dataclasses import dataclass


TRACKS = [
    "AI Engineer",
    "Data Scientist",
    "Data Analyst",
    "Full Stack Developer",
    "Backend Engineer",
    "Cloud/DevOps Engineer",
    "QA Automation Engineer",
    "Cybersecurity Analyst",
    "Business Analyst",
    "UI/UX Designer",
]


TRACK_PROFILES = {
    "AI Engineer": {
        "skills": ["Python", "linear algebra", "probability", "machine learning", "APIs"],
        "traits": ["AI curiosity", "strong programming base", "math comfort"],
    },
    "Data Scientist": {
        "skills": ["Python", "statistics", "probability", "SQL", "machine learning"],
        "traits": ["data reasoning", "math comfort", "experimentation"],
    },
    "Data Analyst": {
        "skills": ["SQL", "spreadsheets", "statistics", "dashboards", "business storytelling"],
        "traits": ["data curiosity", "clear communication", "practical analysis"],
    },
    "Full Stack Developer": {
        "skills": ["HTML/CSS", "JavaScript", "backend APIs", "databases", "deployment basics"],
        "traits": ["programming interest", "product thinking", "end-to-end building"],
    },
    "Backend Engineer": {
        "skills": ["Python/Java/Node", "APIs", "databases", "system design", "testing"],
        "traits": ["deep technical work", "debugging patience", "logic building"],
    },
    "Cloud/DevOps Engineer": {
        "skills": ["Linux", "cloud fundamentals", "CI/CD", "containers", "monitoring"],
        "traits": ["automation", "reliability mindset", "systems thinking"],
    },
    "QA Automation Engineer": {
        "skills": ["testing fundamentals", "Selenium/Playwright", "API testing", "Python/Java", "CI"],
        "traits": ["patience", "quality mindset", "edge-case thinking"],
    },
    "Cybersecurity Analyst": {
        "skills": ["networking", "Linux", "security basics", "threat analysis", "secure coding"],
        "traits": ["risk awareness", "investigation", "attention to detail"],
    },
    "Business Analyst": {
        "skills": ["requirements analysis", "SQL basics", "process mapping", "documentation", "communication"],
        "traits": ["stakeholder communication", "structured thinking", "business curiosity"],
    },
    "UI/UX Designer": {
        "skills": ["user research", "wireframing", "Figma", "accessibility", "design systems"],
        "traits": ["user empathy", "visual thinking", "product sense"],
    },
}


@dataclass(frozen=True)
class ScoreResult:
    scores: dict[str, float]
    primary_track: str
    secondary_track: str
    backup_tracks: list[str]
    patterns: list[str]
    skill_gaps: list[str]


def _numeric(answers: dict, key: str) -> int:
    value = answers.get(key, 3)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 3


def _add(scores: dict[str, float], track: str, points: float) -> None:
    scores[track] += points


def calculate_scores(answers: dict) -> ScoreResult:
    scores = {track: 0.0 for track in TRACKS}

    programming = _numeric(answers, "programming_interest")
    programming_rating = _numeric(answers, "programming_rating")
    debugging = _numeric(answers, "debugging_patience")
    linear_algebra = _numeric(answers, "linear_algebra")
    probability = _numeric(answers, "probability")
    statistics = _numeric(answers, "statistics")
    ai = _numeric(answers, "ai_interest")
    data = _numeric(answers, "data_interest")
    web = _numeric(answers, "web_interest")
    cloud = _numeric(answers, "cloud_interest")
    security = _numeric(answers, "cybersecurity_interest")
    testing = _numeric(answers, "testing_interest")
    business = _numeric(answers, "business_interest")
    uiux = _numeric(answers, "uiux_interest")

    math_average = (linear_algebra + probability + statistics) / 3

    weighted_signals = {
        "AI Engineer": [(ai, 3), (programming, 2), (programming_rating, 2), (linear_algebra, 2), (probability, 1.5), (statistics, 1)],
        "Data Scientist": [(data, 2.5), (statistics, 2.5), (probability, 2), (programming_rating, 1.5), (ai, 1.2)],
        "Data Analyst": [(data, 3), (statistics, 2), (business, 2), (programming_rating, 0.8), (probability, 1)],
        "Full Stack Developer": [(web, 3), (programming, 2.2), (programming_rating, 2), (debugging, 1), (uiux, 0.8)],
        "Backend Engineer": [(programming, 2.5), (programming_rating, 2.5), (debugging, 2), (web, 1), (cloud, 0.8)],
        "Cloud/DevOps Engineer": [(cloud, 3), (debugging, 1.5), (programming_rating, 1.2), (testing, 0.8), (security, 0.8)],
        "QA Automation Engineer": [(testing, 3), (debugging, 2), (programming_rating, 1.5), (web, 0.8), (business, 0.5)],
        "Cybersecurity Analyst": [(security, 3), (debugging, 1.3), (programming_rating, 1), (cloud, 1), (testing, 0.8)],
        "Business Analyst": [(business, 3), (data, 1.5), (statistics, 1), (uiux, 0.8), (programming_rating, 0.4)],
        "UI/UX Designer": [(uiux, 3), (web, 1.2), (business, 1), (programming_rating, 0.4), (data, 0.5)],
    }

    for track, signals in weighted_signals.items():
        for value, weight in signals:
            _add(scores, track, value * weight)

    _apply_choice_scores(scores, answers.get("working_style", ""))
    _apply_choice_scores(scores, answers.get("project_preference", ""))
    _apply_choice_scores(scores, answers.get("career_goal", ""))

    if math_average < 3:
        scores["AI Engineer"] -= 3
        scores["Data Scientist"] -= 2
    if programming_rating < 3:
        for track in ["AI Engineer", "Full Stack Developer", "Backend Engineer", "Cloud/DevOps Engineer", "QA Automation Engineer"]:
            scores[track] -= 1.5

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    primary = ranked[0][0]
    secondary = ranked[1][0]
    backups = [track for track, _ in ranked[2:5]]

    return ScoreResult(
        scores=scores,
        primary_track=primary,
        secondary_track=secondary,
        backup_tracks=backups,
        patterns=_detect_patterns(answers),
        skill_gaps=_skill_gaps(primary, answers),
    )


def _apply_choice_scores(scores: dict[str, float], choice: str) -> None:
    choice_map = {
        "Deep technical problem solving": {"Backend Engineer": 4, "AI Engineer": 2, "Cybersecurity Analyst": 1.5},
        "Visual and creative design work": {"UI/UX Designer": 4, "Full Stack Developer": 1.5},
        "Data exploration and reasoning": {"Data Scientist": 3, "Data Analyst": 3, "AI Engineer": 1},
        "System reliability and operations": {"Cloud/DevOps Engineer": 4, "Backend Engineer": 2, "QA Automation Engineer": 1},
        "Communication, planning, and coordination": {"Business Analyst": 4, "Data Analyst": 1.5, "UI/UX Designer": 1},
        "Investigating risks and edge cases": {"Cybersecurity Analyst": 4, "QA Automation Engineer": 3},
        "Build an AI model or chatbot": {"AI Engineer": 4, "Data Scientist": 2},
        "Analyze a dataset and present insights": {"Data Analyst": 4, "Data Scientist": 3, "Business Analyst": 1.5},
        "Create a full web application": {"Full Stack Developer": 4, "Backend Engineer": 2, "UI/UX Designer": 1},
        "Design cloud deployment pipelines": {"Cloud/DevOps Engineer": 4, "Backend Engineer": 1.5},
        "Automate test cases for an app": {"QA Automation Engineer": 4, "Backend Engineer": 1},
        "Map user journeys and improve screens": {"UI/UX Designer": 4, "Business Analyst": 2},
        "Secure an application and find vulnerabilities": {"Cybersecurity Analyst": 4, "Backend Engineer": 1},
        "Gather requirements for a product team": {"Business Analyst": 4, "Data Analyst": 1},
        "Get a software engineering role quickly": {"Full Stack Developer": 3, "Backend Engineer": 3, "QA Automation Engineer": 1.5},
        "Work on AI or advanced technology": {"AI Engineer": 4, "Data Scientist": 2},
        "Use data to support decisions": {"Data Analyst": 4, "Data Scientist": 2, "Business Analyst": 2},
        "Build secure and reliable systems": {"Cybersecurity Analyst": 3, "Cloud/DevOps Engineer": 3, "Backend Engineer": 2},
        "Blend technology with business communication": {"Business Analyst": 4, "Data Analyst": 2},
        "Create user-friendly digital products": {"UI/UX Designer": 3, "Full Stack Developer": 2, "Business Analyst": 1},
    }
    for track, points in choice_map.get(choice, {}).items():
        _add(scores, track, points)


def _detect_patterns(answers: dict) -> list[str]:
    patterns = []
    math_average = (_numeric(answers, "linear_algebra") + _numeric(answers, "probability") + _numeric(answers, "statistics")) / 3

    if _numeric(answers, "programming_interest") >= 4 and _numeric(answers, "programming_rating") >= 4:
        patterns.append("You show a strong programming signal, which supports engineering-heavy roles.")
    if math_average >= 4:
        patterns.append("Your math comfort is high enough for data science or AI-heavy paths.")
    elif math_average <= 2.5:
        patterns.append("Your math comfort is still developing, so applied or product-facing paths may be easier starting points.")
    if _numeric(answers, "business_interest") >= 4:
        patterns.append("You seem to enjoy connecting technical work with business outcomes.")
    if _numeric(answers, "uiux_interest") >= 4:
        patterns.append("You have a noticeable user-experience and design signal.")
    if _numeric(answers, "debugging_patience") >= 4:
        patterns.append("Your debugging patience is useful for backend, QA, security, and infrastructure work.")
    return patterns or ["Your answers show a balanced profile, so the recommendation weighs both interest and readiness."]


def _skill_gaps(track: str, answers: dict) -> list[str]:
    gaps = []
    programming_rating = _numeric(answers, "programming_rating")
    math_average = (_numeric(answers, "linear_algebra") + _numeric(answers, "probability") + _numeric(answers, "statistics")) / 3

    if programming_rating < 4 and track in {
        "AI Engineer",
        "Full Stack Developer",
        "Backend Engineer",
        "Cloud/DevOps Engineer",
        "QA Automation Engineer",
    }:
        gaps.append("Raise programming fluency through daily problem solving and project work.")
    if math_average < 4 and track in {"AI Engineer", "Data Scientist"}:
        gaps.append("Strengthen linear algebra, probability, and statistics before advanced ML topics.")
    if track in {"Data Analyst", "Data Scientist", "Business Analyst"}:
        gaps.append("Build SQL and dashboard storytelling confidence.")
    if track == "UI/UX Designer":
        gaps.append("Create a portfolio with research notes, wireframes, prototypes, and usability improvements.")
    if track == "Cloud/DevOps Engineer":
        gaps.append("Practice Linux, cloud basics, CI/CD, containers, and monitoring.")
    if track == "Cybersecurity Analyst":
        gaps.append("Build foundations in networking, Linux, security terminology, and threat analysis.")
    if track == "QA Automation Engineer":
        gaps.append("Learn test design, automation frameworks, API testing, and CI integration.")
    return gaps or ["Convert your interest into evidence through 2-3 portfolio projects."]
