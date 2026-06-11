# Architecture

HelpDeskLite uses a conventional Flask structure with SQLAlchemy models, service classes, route blueprints, and Jinja templates.

## Current Architecture

- `app.py` at the repository root starts the app.
- `helpdesk_lite/app.py` builds the Flask application and registers blueprints.
- `helpdesk_lite/database.py` owns the SQLAlchemy extension and database initialization.
- `helpdesk_lite/models.py` defines `User`, `Issue`, and `Comment`.
- `helpdesk_lite/routes/` contains web routes for the dashboard, issues, and users.
- `helpdesk_lite/services/` contains business logic for users, issues, comments, and dashboard data.
- `helpdesk_lite/templates/` contains Jinja templates.
- `helpdesk_lite/tests/` contains pytest coverage for common workflows.

## Known Weaknesses

The codebase intentionally resembles a competent project after several months of feature growth.

- Some route handlers do validation and workflow decisions that also exist in services.
- `IssueService` mixes persistence, validation, formatting, and workflow rules.
- There is no repository layer, so services query SQLAlchemy models directly.
- Validation is basic and inconsistent between create and edit paths.
- Error handling mostly returns string lists and redirects with flash messages.
- Dashboard queries are inefficient and repeat similar filters.
- There is no authorization model.
- There is no pagination for user or issue lists.
- There is no audit trail for issue changes.
- Search behavior is database-specific.

## Future Improvements

Good workshop refactoring targets include:

- Extract an `IssueRepository` and `UserRepository`.
- Move row formatting out of `IssueService`.
- Unify create/edit validation.
- Add authorization checks for issue mutation routes.
- Add pagination to issue and user lists.
- Replace case-sensitive SQLite `GLOB` search with case-insensitive search.
- Add an audit logging service for status, assignment, and edit events.
- Consolidate dashboard metrics into fewer queries.
- Add API routes and separate them from HTML routes.
- Improve tests around routes, empty descriptions, dashboard performance, and search.
