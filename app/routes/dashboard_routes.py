from flask import Blueprint, render_template
from flask_login import login_required

from app.services.dashboard_service import DashboardService

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    service = DashboardService()
    dashboard = service.get_dashboard_data()
    return render_template("dashboard/index.html", dashboard=dashboard)
