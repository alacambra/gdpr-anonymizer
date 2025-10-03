.PHONY: help install install-dev test test-cov lint format type-check clean build docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package in development mode"
	@echo "  install-dev  Install with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code (black, isort)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  docs         Build documentation"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,test,docs]"

# Testing
test:
	pytest

test-cov:
	pytest --cov=gdpr_anonymizer --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 gdpr_anonymizer tests

format:
	black gdpr_anonymizer tests
	isort gdpr_anonymizer tests

type-check:
	mypy gdpr_anonymizer

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Documentation
docs:
	cd docs && make html

# Development workflow
dev-setup: install-dev
	pre-commit install

# Quick check (runs all quality checks)
check: lint type-check test

# Release preparation
pre-release: format lint type-check test-cov build