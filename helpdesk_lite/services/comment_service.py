from helpdesk_lite.database import db
from helpdesk_lite.models import Comment, Issue
from helpdesk_lite.validators import validate_comment_payload


class CommentService:
    def add_comment(self, issue_id, author_name, body):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return None, ["Issue not found."]

        errors = validate_comment_payload(author_name, body)
        if errors:
            return None, errors

        comment = Comment(
            issue_id=issue.id,
            author_name=author_name.strip(),
            body=body.strip(),
        )
        db.session.add(comment)
        db.session.commit()
        return comment, []

    def list_for_issue(self, issue_id):
        return (
            Comment.query.filter_by(issue_id=issue_id)
            .order_by(Comment.created_at.asc())
            .all()
        )
