# BPU Nexus Backend

FastAPI backend for the BPU Nexus platform.

## Technology
- Python and FastAPI
- PostgreSQL
- SQLAlchemy and Alembic
- JWT authentication
- Ollama AI integration (planned)
- Google Drive document ingestion (planned)

## Local development

Activate the virtual environment:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Run database migrations:

    alembic upgrade head

Start the API:

    uvicorn app.main:app --reload

API documentation:

    http://127.0.0.1:8000/docs
