# The Evolution of Todo - Phase I

A Python-based in-memory Todo Console Application tailored for the "Evolution of Todo" Hackathon.

## Features
- **Add**: Create new tasks with title and optional description.
- **List**: View all tasks with their status.
- **Update**: Modify task details.
- **Complete**: Mark tasks as done.
- **Delete**: Remove tasks.
- **Spec-Driven**: Generated following strict specification rules.

## Setup & Running

### Prerequisites
- Python 3.13+
- `uv` (recommended) or standard `pip`

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   uv sync
   # OR
   pip install -r requirements.txt  # (If you export requirements)
   # Or just manually:
   pip install rich
   ```

### Usage
Run the application:
```bash
python src/main.py
```
OR with uv:
```bash
uv run src/main.py
```

### Commands
- `add <title> [description]`
- `list`
- `update <id> [title] [description]`
- `complete <id>`
- `delete <id>`
- `exit`

## Project Structure
- `specs/`: Project specifications.
- `src/`: Source code.
- `tests/`: Verification scripts.
