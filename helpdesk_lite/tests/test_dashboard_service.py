from helpdesk_lite.services.dashboard_service import DashboardService
from helpdesk_lite.services.issue_service import IssueService


def test_dashboard_counts_open_and_closed(app):
    issues = IssueService()
    open_issue, _ = issues.create_issue("Open", "Open desc", "A", "low")
    closed_issue, _ = issues.create_issue("Closed", "Closed desc", "B", "low")
    issues.close_issue(closed_issue.id)

    data = DashboardService().get_dashboard_data()

    assert data["open_count"] == 1
    assert data["closed_count"] == 1
    assert open_issue.title in data["open_titles"]


def test_dashboard_returns_recent_issues(app):
    issues = IssueService()
    issues.create_issue("First", "Desc", "A", "low")
    latest, _ = issues.create_issue("Latest", "Desc", "A", "high")

    data = DashboardService().get_dashboard_data()

    assert data["recent_issues"][0].id == latest.id
