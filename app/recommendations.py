"""Recommendation narratives and 3-month roadmaps."""

from __future__ import annotations

from app.scoring import ScoreResult, TRACK_PROFILES


ROADMAPS = {
    "AI Engineer": [
        "Month 1: Python, NumPy, pandas, linear algebra refresh, and small data preprocessing tasks.",
        "Month 2: Supervised learning, model evaluation, scikit-learn, and one prediction project.",
        "Month 3: Neural network basics, LLM/API integration, model deployment with FastAPI, and a portfolio demo.",
    ],
    "Data Scientist": [
        "Month 1: Python, SQL, statistics, probability, and exploratory data analysis.",
        "Month 2: Machine learning, experiment design, feature engineering, and model evaluation.",
        "Month 3: Build two end-to-end projects with notebooks, dashboards, and written business conclusions.",
    ],
    "Data Analyst": [
        "Month 1: SQL, spreadsheets, descriptive statistics, and clean chart design.",
        "Month 2: Dashboarding with Power BI/Tableau/Streamlit and business case analysis.",
        "Month 3: Build a portfolio with 3 case studies: sales, product, and operations analytics.",
    ],
    "Full Stack Developer": [
        "Month 1: HTML, CSS, JavaScript, Git, and responsive UI fundamentals.",
        "Month 2: Backend APIs, databases, authentication, and CRUD application patterns.",
        "Month 3: Ship a deployed full-stack project with tests, documentation, and a clean README.",
    ],
    "Backend Engineer": [
        "Month 1: Strengthen one backend language, data structures, Git, and API basics.",
        "Month 2: Databases, authentication, testing, caching, and error handling.",
        "Month 3: Build a production-style API with docs, tests, logs, and deployment.",
    ],
    "Cloud/DevOps Engineer": [
        "Month 1: Linux, networking basics, shell scripting, and Git workflows.",
        "Month 2: Cloud fundamentals, Docker, CI/CD, environment variables, and deployment.",
        "Month 3: Monitoring, infrastructure-as-code basics, and a deployed app pipeline project.",
    ],
    "QA Automation Engineer": [
        "Month 1: Manual testing concepts, test cases, bug reports, and programming basics.",
        "Month 2: UI automation with Selenium/Playwright and API testing with Postman/Pytest.",
        "Month 3: CI test execution, reporting, and an automation portfolio for a sample app.",
    ],
    "Cybersecurity Analyst": [
        "Month 1: Networking, Linux, web security basics, and common vulnerabilities.",
        "Month 2: Log analysis, threat modeling, secure coding, and hands-on labs.",
        "Month 3: Build a security portfolio with vulnerability reports and remediation notes.",
    ],
    "Business Analyst": [
        "Month 1: Requirements gathering, user stories, process maps, and stakeholder notes.",
        "Month 2: SQL basics, metrics, dashboards, and business case writing.",
        "Month 3: Create 3 product requirement documents with mock data insights and acceptance criteria.",
    ],
    "UI/UX Designer": [
        "Month 1: Design principles, Figma, user research, accessibility, and wireframing.",
        "Month 2: Prototyping, usability testing, design systems, and UI critique practice.",
        "Month 3: Publish 2-3 case studies showing problem, research, iterations, and final designs.",
    ],
}


def build_recommendation(result: ScoreResult) -> dict:
    primary_profile = TRACK_PROFILES[result.primary_track]
    secondary_profile = TRACK_PROFILES[result.secondary_track]

    reason = (
        f"{result.primary_track} is the best-fit starting track because your answers align with "
        f"{', '.join(primary_profile['traits'])}. The secondary fit is {result.secondary_track}, "
        f"which also matches {', '.join(secondary_profile['traits'][:2])}."
    )

    return {
        "best_fit_career_track": result.primary_track,
        "secondary_track": result.secondary_track,
        "reason": reason,
        "patterns": result.patterns,
        "skill_gaps": result.skill_gaps,
        "three_month_learning_roadmap": ROADMAPS[result.primary_track],
        "backup_career_tracks": result.backup_tracks,
        "scores": result.scores,
    }
