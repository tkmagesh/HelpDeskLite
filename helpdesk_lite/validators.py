VALID_PRIORITIES = {"low", "medium", "high", "urgent"}


def validate_user_payload(name, email):
    errors = []
    if not name or not name.strip():
        errors.append("Name is required.")
    if not email or "@" not in email:
        errors.append("A valid email is required.")
    return errors


def validate_issue_payload(title, description, reporter_name, priority):
    errors = []
    if not title or not title.strip():
        errors.append("Title is required.")
    if not description or not description.strip():
        errors.append("Description is required.")
    if not reporter_name or not reporter_name.strip():
        errors.append("Reporter name is required.")
    if priority not in VALID_PRIORITIES:
        errors.append("Priority must be low, medium, high, or urgent.")
    return errors


def validate_comment_payload(author_name, body):
    errors = []
    if not author_name or not author_name.strip():
        errors.append("Author name is required.")
    if not body or not body.strip():
        errors.append("Comment body is required.")
    return errors
