from flask import Blueprint, render_template

from helpdesk_lite.services.dashboard_service import DashboardService


dashboard_bp = Blueprint("dashboard", __name__)
dashboard_service = DashboardService()


@dashboard_bp.get("/")
def index():
    data = dashboard_service.get_dashboard_data()
    return render_template("dashboard.html", dashboard=data)
