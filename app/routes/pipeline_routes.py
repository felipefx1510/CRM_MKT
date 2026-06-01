from flask import Blueprint, render_template
from flask_login import login_required

from app.constants import LEAD_STATUSES
from app.services.lead_service import LeadService

bp = Blueprint("pipeline", __name__)


@bp.route("/pipeline")
@login_required
def board():
    service = LeadService()
    leads_by_status = service.list_by_status()
    return render_template(
        "pipeline/board.html",
        statuses=LEAD_STATUSES,
        leads_by_status=leads_by_status,
    )
