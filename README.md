# HelpDeskLite

HelpDeskLite is a small Python Flask issue tracker built for GitHub Copilot workshops. It is intentionally realistic rather than pristine: the code is understandable, runnable, and tested, while still containing technical debt for planning, review, debugging, refactoring, and architecture exercises.

## Features

- Create and list users
- Create, view, edit, close, reopen, assign, and search issues
- Add and view comments on issues
- Dashboard with open count, closed count, and recently updated issues

## Setup

Use Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

The default database is SQLite and is created automatically as `helpdesklite.db` through Flask-SQLAlchemy.

## Run Tests

```bash
pytest
```

The test suite uses an in-memory SQLite database.

## Workshop Notes

This repository is designed for classroom use. It includes duplicated logic, uneven service boundaries, TODO comments, and documented defects. See [ARCHITECTURE.md](ARCHITECTURE.md) and [INSTRUCTOR_NOTES.md](INSTRUCTOR_NOTES.md) before using it in a workshop.

Known low-risk defects are intentionally present:

- Search is case sensitive.
- Dashboard performs unnecessary queries.
- Issue editing allows empty descriptions.
