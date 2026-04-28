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
