# Makefile for Thai Food Image Classification API

.PHONY: help install install-dev test lint format clean run

help:
	@echo "Available commands:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make test           Run tests with coverage"
	@echo "  make lint           Run linter (flake8)"
	@echo "  make format         Format code with black"
	@echo "  make clean          Remove build artifacts and cache"
	@echo "  make run            Run the application locally"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

lint:
	flake8 .

format:
	black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf dist/
	rm -rf build/

run:
	python index.py

check: lint test
	@echo "All checks passed!"
