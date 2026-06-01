from flask import Blueprint, render_template
from flask_login import login_required

from app.services.report_service import ReportService

bp = Blueprint("reports", __name__)


@bp.route("/reports")
@login_required
def index():
    service = ReportService()
    report = service.get_report_data()
    return render_template("reports/index.html", report=report)
