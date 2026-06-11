from datetime import datetime, timezone

from helpdesk_lite.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    assigned_issues = db.relationship(
        "Issue", back_populates="assignee", foreign_keys="Issue.assignee_id"
    )

    def __repr__(self):
        return f"<User {self.email}>"


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="open", nullable=False)
    priority = db.Column(db.String(30), default="medium", nullable=False)
    reporter_name = db.Column(db.String(120), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    closed_at = db.Column(db.DateTime, nullable=True)

    assignee = db.relationship(
        "User", back_populates="assigned_issues", foreign_keys=[assignee_id]
    )
    comments = db.relationship(
        "Comment", back_populates="issue", cascade="all, delete-orphan"
    )

    def is_open(self):
        return self.status == "open"

    def __repr__(self):
        return f"<Issue {self.id}: {self.title}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey("issues.id"), nullable=False)
    author_name = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    issue = db.relationship("Issue", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id} on issue {self.issue_id}>"
