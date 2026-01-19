# Default: list available commands
default:
    @just --list

# Run tests
test *args:
    uv run pytest -vv {{ args }}

# Run linter
lint:
    uv run ruff check .

# Fix lint errors
lint-fix:
    uv run ruff check . --fix

# Format code
format:
    uv run ruff format .

# Check formatting (no changes)
format-check:
    uv run ruff format --check .

# Run type checking
type-check:
    uv run mypy src/switrs_to_sqlite/ tests/ scripts/

# Run all checks (CI)
check: lint format-check type-check test

# Build package
build:
    uv build

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info .pytest_cache .ruff_cache

# Install dependencies
sync:
    uv sync --dev

# Show CLI help
help:
    uv run switrs_to_sqlite --help
