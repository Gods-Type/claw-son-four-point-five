# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

AI research, implementation, and educational platform focused on addressing AI limitations. Three top-level components: `research/` (analysis), `implementation/` (ML solutions + API), and `education/` (learning platform with web frontend/backend).

## Build, Test, and Lint Commands

### Python (from repo root)

```bash
# Run all tests with coverage
make test
# or directly:
pytest -v --cov=implementation/src --cov=research --cov=education --cov-report=html --cov-report=term

# Run a single test file
pytest implementation/tests/path/to/test_file.py -v

# Run a specific test
pytest implementation/tests/path/to/test_file.py::TestClass::test_method -v

# Run tests by marker (unit, integration, slow)
pytest -m unit
pytest -m "not slow"

# Lint
make lint
# Runs: flake8, mypy (on implementation/src), bandit

# Format
make format
# Runs: black, isort (on implementation/src, research, education)

# Full quality check (lint + test)
make check
```

### Education Frontend (from `education/platform/frontend/`)

```bash
npm run dev          # Dev server (port 3000)
npm run build        # Production build
npm run lint         # ESLint
npm run type-check   # TypeScript type checking
npm run test         # Jest tests
npm run format       # Prettier
npm run format:check # Check formatting
```

### Docker Services

```bash
make dev          # Start postgres, redis, mlflow
make dev-all      # Start all services (API :8000, frontend :3000, MLflow :5000, Jupyter :8888)
make dev-stop     # Stop all services
```

### Database Migrations (from `implementation/`)

```bash
alembic upgrade head                         # Run migrations
alembic revision --autogenerate -m "message"  # Create migration
```

## Architecture

### Base Class Hierarchy (`implementation/src/core/base/__init__.py`)

All models, pipelines, and reasoning components inherit from abstract base classes defined in `implementation/src/core/base/`. New implementations must satisfy these interfaces:

- **BaseModel**: `fit()`, `predict()`, `explain()`, `evaluate()` — all models must provide explainability via `explain()`
- **BasePipeline**: `fit()`, `transform()`, `get_params()`, `set_params()`
- **BaseReasoner**: `reason()`, `add_knowledge()`, `explain_reasoning()`
- **BaseExplainer**: `explain_instance()`, `explain_global()`, `visualize_explanation()`
- **BaseDataProcessor**: `fit()`, `transform()`, `inverse_transform()`
- **BaseEvaluator**: `evaluate_classification()`, `evaluate_regression()`, `evaluate_explainability()`, `evaluate_robustness()`

### Neuro-Symbolic Pattern

The core ML approach combines neural networks with symbolic reasoning (see `implementation/src/models/neuro_symbolic_classifier.py`). Models follow a two-branch architecture:
1. Neural network processes input features
2. Symbolic reasoner (extending `BaseReasoner`) applies rule-based logic
3. Integration layer fuses outputs via late fusion or attention fusion

This pattern should be followed when adding new hybrid models.

### Two FastAPI Applications

- **Implementation API** (`implementation/src/main.py`, port 8000): Model serving, predictions with built-in explainability (`/predict` with `explanation_required`), experiment listing
- **Education API** (`education/platform/backend/src/main.py`, port 8001): User auth (JWT), learning paths, tutorials, exercises, progress tracking, assessments

Both use the lifespan pattern for startup/shutdown, CORSMiddleware, and GZipMiddleware.

### Education Frontend

Next.js 14 + TypeScript + Tailwind CSS. Uses Zustand for state, Monaco Editor for code editing, Radix UI for components, Chart.js/D3 for visualization. Located at `education/platform/frontend/`.

### Experiment Tracking

`implementation/src/utils/experiment_tracking.py` provides `ExperimentTracker` (MLflow wrapper) and `ExperimentManager` (config-driven experiment execution). Experiment configs are YAML/JSON files in `implementation/experiments/configs/`.

### Infrastructure

Docker Compose orchestrates: PostgreSQL (5432), Redis (6379), MLflow (5000), Jupyter (8888), implementation API (8000), education API (8001), frontend (3000), Celery workers/beat. CI/CD runs on GitHub Actions (`.github/workflows/ci-cd.yml`) testing across Python 3.9-3.11.

## Code Style

- **Python**: black (line-length 88, target py39), isort (profile "black"), flake8 (E203/W503 ignored), mypy with strict settings (`disallow_untyped_defs`, `disallow_incomplete_defs`, `check_untyped_defs`, `strict_equality`)
- **TypeScript/JS**: prettier + eslint-config-next, lint-staged via husky
- mypy ignores missing imports for: torch, tensorflow, sklearn, matplotlib, seaborn, mlflow, wandb
- pytest markers: `slow`, `integration`, `unit` (use `--strict-markers`)
- Test paths: `implementation/tests/`, `research/analysis/tests/`, `education/tests/`
- Coverage target: 80% minimum (`make test-cov`)

## Environment Setup

Copy `.env.example` to `.env`. Key variables: `DATABASE_URL`, `REDIS_URL`, `MLFLOW_TRACKING_URI`, `API_SECRET_KEY`, `WANDB_PROJECT`. See `.env.example` for all required variables.
