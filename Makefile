# Makefile for claw-son-four-point-five
# Provides convenient commands for development, testing, and deployment

.PHONY: help setup install test lint format clean docs build deploy dev

# Default target
help:
	@echo "Available commands:"
	@echo "  setup     - Set up development environment"
	@echo "  install   - Install dependencies"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  clean     - Clean build artifacts"
	@echo "  docs      - Build documentation"
	@echo "  build     - Build project"
	@echo "  deploy    - Deploy to production"
	@echo "  dev       - Start development environment"
	@echo "  help      - Show this help message"

# Setup development environment
setup:
	@echo "Setting up development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate     (Windows)"
	cp .env.example .env
	@echo "Environment file created. Please edit .env with your values."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "Development environment setup complete!"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "Dependencies installed."

# Run tests
test:
	@echo "Running tests..."
	pytest -v --cov=implementation/src --cov=research --cov=education --cov-report=html --cov-report=term

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	pytest -v --cov=implementation/src --cov=research --cov=education --cov-report=html --cov-report=term --cov-fail-under=80

# Run linting
lint:
	@echo "Running linting..."
	flake8 implementation/src research education
	mypy implementation/src
	bandit -r implementation/src
	@echo "Linting complete."

# Format code
format:
	@echo "Formatting code..."
	black implementation/src research education
	isort implementation/src research education
	@echo "Code formatted."

# Check code quality
check: lint test
	@echo "Code quality checks complete."

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "Build artifacts cleaned."

# Build documentation
docs:
	@echo "Building documentation..."
	@echo "Building Sphinx documentation..."
	cd docs && make html
	@echo "Documentation built in docs/_build/html/"

# Serve documentation locally
docs-serve:
	@echo "Serving documentation locally..."
	cd docs/_build/html && python -m http.server 8080

# Build project for distribution
build:
	@echo "Building project..."
	python -m build
	@echo "Project built in dist/"

# Deploy to production
deploy:
	@echo "Deploying to production..."
	@echo "Deployment not yet implemented."
	@echo "Please implement deployment script for your target environment."

# Start development environment
dev:
	@echo "Starting development environment..."
	docker-compose up -d postgres redis mlflow
	@echo "Services started. Use 'make dev-all' to include API and frontend."

# Start all development services
dev-all:
	@echo "Starting all development services..."
	docker-compose up -d
	@echo "All services started."
	@echo "Jupyter Lab: http://localhost:8888?token=claw_son_token"
	@echo "API: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "MLflow: http://localhost:5000"

# Stop development services
dev-stop:
	@echo "Stopping development services..."
	docker-compose down
	@echo "Development services stopped."

# View logs
logs:
	docker-compose logs -f

# Backup data
backup:
	@echo "Backing up data..."
	mkdir -p backups
	docker exec claw_son_postgres pg_dump -U postgres claw_son_dev > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

# Restore data from backup
restore:
	@echo "Restoring data from backup..."
	@read -p "Enter backup file path: " backup_file; \
	docker exec -i claw_son_postgres psql -U postgres claw_son_dev < $$backup_file
	@echo "Data restored."

# Run research analysis
research:
	@echo "Running research analysis..."
	cd research/analysis && jupyter lab --port=8889 --no-browser

# Run ML experiments
experiment:
	@echo "Running ML experiments..."
	cd implementation && python -m experiments.run_experiment

# Update dependencies
update-deps:
	@echo "Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip install --upgrade -r requirements-dev.txt
	@echo "Dependencies updated."

# Security audit
security:
	@echo "Running security audit..."
	safety check
	bandit -r implementation/src
	@echo "Security audit complete."

# Database migrations
migrate:
	@echo "Running database migrations..."
	cd implementation && alembic upgrade head
	@echo "Migrations complete."

# Create new database migration
migration:
	@echo "Creating new database migration..."
	@read -p "Enter migration message: " message; \
	cd implementation && alembic revision --autogenerate -m "$$message"
	@echo "Migration created."