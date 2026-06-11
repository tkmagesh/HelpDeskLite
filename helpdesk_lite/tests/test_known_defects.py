from helpdesk_lite.services.issue_service import IssueService


def test_edit_allows_empty_description_known_training_defect(sample_issue):
    service = IssueService()

    issue, errors = service.edit_issue(sample_issue.id, "Still broken", "", "high")

    assert errors == []
    assert issue.description == ""


def test_search_case_sensitivity_known_training_defect(app):
    service = IssueService()
    service.create_issue("VPN Access", "Cannot connect.", "Sam", "medium")

    issues = service.list_issues(search_term="vpn")

    assert issues == []
