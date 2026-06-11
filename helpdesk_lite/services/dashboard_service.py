from helpdesk_lite.models import Issue


class DashboardService:
    def get_dashboard_data(self):
        # Defect for exercises: this does more queries than needed and repeats
        # filtering work that could be consolidated.
        open_count = Issue.query.filter_by(status="open").count()
        closed_count = Issue.query.filter_by(status="closed").count()
        recent = Issue.query.order_by(Issue.updated_at.desc()).limit(5).all()
        open_issues = Issue.query.filter_by(status="open").all()
        closed_issues = Issue.query.filter_by(status="closed").all()

        # TODO caching: this is recalculated on every page load.
        return {
            "open_count": open_count,
            "closed_count": closed_count,
            "recent_issues": recent,
            "open_titles": [issue.title for issue in open_issues],
            "closed_titles": [issue.title for issue in closed_issues],
        }
