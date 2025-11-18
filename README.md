# FastAPI Calculations Assignment - CI Clean Version

- Calculator web UI at `/` and `/calc`
- Calculation model with SQLAlchemy
- Pydantic v2 schemas with validation
- Factory pattern for operations
- Unit + integration tests with coverage
- Dockerfile + docker-compose
- GitHub Actions CI that runs `pytest` and pushes a Docker image on `main`

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/

## Tests with coverage

```bash
pytest
```

Coverage is configured via pytest.ini.

## Docker

```bash
docker-compose up --build
```

Then visit: http://localhost:8000/

## GitHub Actions

Add secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` and push to `main`
to trigger CI build, tests, and Docker Hub push.
