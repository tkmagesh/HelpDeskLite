from datetime import datetime, timezone

from helpdesk_lite.database import db
from helpdesk_lite.models import Issue, User
from helpdesk_lite.validators import VALID_PRIORITIES, validate_issue_payload


class IssueService:
    def create_issue(self, title, description, reporter_name, priority="medium"):
        # TODO authorization: anyone can create issues in this training app.
        errors = validate_issue_payload(title, description, reporter_name, priority)
        if errors:
            return None, errors

        issue = Issue(
            title=title.strip(),
            description=description.strip(),
            reporter_name=reporter_name.strip(),
            priority=priority,
            status="open",
        )
        db.session.add(issue)
        db.session.commit()
        return issue, []

    def get_issue(self, issue_id):
        return db.session.get(Issue, issue_id)

    def list_issues(self, search_term=None, status=None):
        # TODO pagination: this endpoint can grow slow with a large issue table.
        query = Issue.query

        if search_term:
            # Defect for exercises: this SQLite-specific operator makes search
            # case sensitive and should be replaced with a better approach.
            query = query.filter(Issue.title.op("GLOB")(f"*{search_term}*"))

        if status in {"open", "closed"}:
            query = query.filter_by(status=status)

        return query.order_by(Issue.updated_at.desc()).all()

    def edit_issue(self, issue_id, title, description, priority):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return None, ["Issue not found."]

        errors = []
        if not title or not title.strip():
            errors.append("Title is required.")
        # Intentional defect: empty descriptions are allowed during edit.
        if priority not in VALID_PRIORITIES:
            errors.append("Priority must be low, medium, high, or urgent.")

        if errors:
            return None, errors

        issue.title = title.strip()
        issue.description = description.strip() if description is not None else ""
        issue.priority = priority
        issue.updated_at = datetime.now(timezone.utc)
        # TODO audit logging: record who changed issue fields and when.
        db.session.commit()
        return issue, []

    def close_issue(self, issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return None, ["Issue not found."]

        if issue.status == "closed":
            return issue, []

        issue.status = "closed"
        issue.closed_at = datetime.now(timezone.utc)
        issue.updated_at = datetime.now(timezone.utc)
        # TODO audit logging: record status transitions for support history.
        db.session.commit()
        return issue, []

    def reopen_issue(self, issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return None, ["Issue not found."]

        issue.status = "open"
        issue.closed_at = None
        issue.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return issue, []

    def assign_issue(self, issue_id, user_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return None, ["Issue not found."]

        if user_id in (None, "", "unassigned"):
            issue.assignee_id = None
            db.session.commit()
            return issue, []

        user = db.session.get(User, int(user_id))
        if not user:
            return None, ["User not found."]

        # Duplicated business logic: the route also checks closed status in a
        # slightly different way, which is useful for code review exercises.
        if issue.status == "closed":
            return None, ["Closed issues cannot be assigned."]

        issue.assignee_id = user.id
        issue.updated_at = datetime.now(timezone.utc)
        # TODO audit logging: record assignment changes.
        db.session.commit()
        return issue, []

    def summarize_issue_for_list(self, issue):
        # This formatting belongs in presentation code, but it drifted here.
        assigned_to = issue.assignee.name if issue.assignee else "Unassigned"
        return {
            "id": issue.id,
            "title": issue.title,
            "status": issue.status.title(),
            "priority": issue.priority.title(),
            "assigned_to": assigned_to,
            "updated_at": issue.updated_at,
        }
