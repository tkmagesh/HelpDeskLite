from helpdesk_lite.services.issue_service import IssueService


def test_create_issue_success(app):
    service = IssueService()

    issue, errors = service.create_issue(
        "Laptop broken", "Screen flickers intermittently.", "Linus", "medium"
    )

    assert errors == []
    assert issue.id is not None
    assert issue.status == "open"


def test_create_issue_validates_required_fields(app):
    service = IssueService()

    issue, errors = service.create_issue("", "", "", "medium")

    assert issue is None
    assert "Title is required." in errors
    assert "Description is required." in errors
    assert "Reporter name is required." in errors


def test_create_issue_rejects_unknown_priority(app):
    service = IssueService()

    issue, errors = service.create_issue(
        "Laptop broken", "Screen flickers.", "Linus", "extreme"
    )

    assert issue is None
    assert "Priority must be low, medium, high, or urgent." in errors


def test_list_issues_filters_by_status(app):
    service = IssueService()
    open_issue, _ = service.create_issue("Open item", "A", "Reporter", "low")
    closed_issue, _ = service.create_issue("Closed item", "B", "Reporter", "low")
    service.close_issue(closed_issue.id)

    issues = service.list_issues(status="open")

    assert [issue.id for issue in issues] == [open_issue.id]


def test_search_issues_by_title(app):
    service = IssueService()
    service.create_issue("VPN access", "Cannot connect.", "Sam", "medium")
    service.create_issue("Monitor cable", "Needs HDMI cable.", "Sam", "low")

    issues = service.list_issues(search_term="VPN")

    assert len(issues) == 1
    assert issues[0].title == "VPN access"


def test_edit_issue_changes_title_and_priority(sample_issue):
    service = IssueService()

    issue, errors = service.edit_issue(
        sample_issue.id, "Printer makes noise", "Still jammed.", "urgent"
    )

    assert errors == []
    assert issue.title == "Printer makes noise"
    assert issue.priority == "urgent"


def test_close_issue_sets_status(sample_issue):
    service = IssueService()

    issue, errors = service.close_issue(sample_issue.id)

    assert errors == []
    assert issue.status == "closed"
    assert issue.closed_at is not None


def test_reopen_issue_clears_closed_at(sample_issue):
    service = IssueService()
    service.close_issue(sample_issue.id)

    issue, errors = service.reopen_issue(sample_issue.id)

    assert errors == []
    assert issue.status == "open"
    assert issue.closed_at is None


def test_assign_issue_to_user(sample_issue, sample_user):
    service = IssueService()

    issue, errors = service.assign_issue(sample_issue.id, sample_user.id)

    assert errors == []
    assert issue.assignee_id == sample_user.id


def test_assign_closed_issue_is_rejected(sample_issue, sample_user):
    service = IssueService()
    service.close_issue(sample_issue.id)

    issue, errors = service.assign_issue(sample_issue.id, sample_user.id)

    assert issue is None
    assert errors == ["Closed issues cannot be assigned."]
