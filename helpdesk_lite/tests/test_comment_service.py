from helpdesk_lite.services.comment_service import CommentService


def test_add_comment_success(sample_issue):
    service = CommentService()

    comment, errors = service.add_comment(sample_issue.id, "Mina", "I can reproduce it.")

    assert errors == []
    assert comment.id is not None
    assert comment.issue_id == sample_issue.id


def test_add_comment_requires_body(sample_issue):
    service = CommentService()

    comment, errors = service.add_comment(sample_issue.id, "Mina", "")

    assert comment is None
    assert errors == ["Comment body is required."]


def test_list_comments_for_issue(sample_issue):
    service = CommentService()
    service.add_comment(sample_issue.id, "Mina", "First.")
    service.add_comment(sample_issue.id, "Ravi", "Second.")

    comments = service.list_for_issue(sample_issue.id)

    assert [comment.body for comment in comments] == ["First.", "Second."]
