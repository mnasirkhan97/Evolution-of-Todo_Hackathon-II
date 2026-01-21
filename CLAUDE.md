# CLAUDE.md - Developer Instructions

## Build & Test
- **Run App**: `python src/main.py` OR `uv run src/main.py`
- **Install Dependencies**: `uv sync`
- **Test**: `pytest` (if applicable)

## Project Architecture
- **Phase I**: In-memory Python Console App.
- **Structure**:
  - `specs/`: Markdown specifications for features.
  - `src/`: Python source code.

## Coding Standards
- **Spec-Driven**: Read the spec before writing code.
- **Typing**: Use standard Python type hinting.
- **Style**: Follow PEP 8.
- **Documentation**: Docstrings for all functions and classes.
