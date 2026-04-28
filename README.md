# Career Guidance AI Agent

Counselor-style career guidance app for engineering students. It asks 18 structured questions, analyzes patterns, and recommends:

- Best-fit career track
- Secondary track
- Reason for recommendation
- Skill gaps
- 3-month learning roadmap
- Backup career tracks

## Stack

- FastAPI backend
- Streamlit frontend
- SQLite database
- Modular Python scoring and recommendation engine

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

For the local FastAPI backend, install the backend extras:

```bash
pip install -r requirements-backend.txt
```

Start the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Start the frontend in another terminal:

```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

Open:

```text
http://localhost:8501
```

## Deploy On Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to Streamlit Community Cloud and create a new app.
3. Select the repository, branch, and set the main file path to:

```text
streamlit_app.py
```

4. Deploy.

The deployed Streamlit app runs standalone. It uses the same modular scoring and recommendation engine, and saves assessments to SQLite from the Streamlit process. The FastAPI backend remains available for local/API use, but is not required for Streamlit Cloud.

Streamlit Cloud uses `requirements.txt`, which intentionally excludes FastAPI and Pydantic so deployment does not need to build `pydantic-core`.
