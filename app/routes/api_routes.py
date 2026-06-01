from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.services.dashboard_service import DashboardService
from app.services.lead_service import LeadService
from app.services.report_service import ReportService

bp = Blueprint("api", __name__)


@bp.route("/leads", methods=["GET"])
@login_required
def get_leads():
    service = LeadService()
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    status = request.args.get("status", "", type=str)
    origem = request.args.get("origem", "", type=str)
    pagination = service.list_paginated(
        search=search or None,
        status=status or None,
        origem=origem or None,
        page=page,
        per_page=20,
    )
    return jsonify({
        "items": [lead.to_dict() for lead in pagination.items],
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
    })


@bp.route("/leads", methods=["POST"])
@login_required
def create_lead():
    data = request.get_json(silent=True) or {}
    allowed_fields = {
        "nome",
        "email",
        "telefone",
        "empresa",
        "origem",
        "mensagem",
        "segmento",
        "interesse",
        "status",
    }
    payload = {key: value for key, value in data.items() if key in allowed_fields}
    required = {"nome", "email", "origem", "interesse"}
    if not required.issubset(payload):
        return jsonify({"error": "Campos obrigatorios ausentes."}), 400

    service = LeadService()
    lead = service.create_lead(payload)
    return jsonify(lead.to_dict()), 201


@bp.route("/leads/<int:lead_id>", methods=["GET"])
@login_required
def get_lead(lead_id):
    service = LeadService()
    lead = service.get_lead(lead_id)
    if not lead:
        return jsonify({"error": "Lead nao encontrado."}), 404
    return jsonify(lead.to_dict())


@bp.route("/leads/<int:lead_id>", methods=["PUT"])
@login_required
def update_lead(lead_id):
    data = request.get_json(silent=True) or {}
    allowed_fields = {
        "nome",
        "email",
        "telefone",
        "empresa",
        "origem",
        "mensagem",
        "segmento",
        "interesse",
        "status",
        "resumo_ia",
    }
    payload = {key: value for key, value in data.items() if key in allowed_fields}
    service = LeadService()
    lead = service.update_lead(lead_id, payload)
    if not lead:
        return jsonify({"error": "Lead nao encontrado."}), 404
    return jsonify(lead.to_dict())


@bp.route("/leads/<int:lead_id>", methods=["DELETE"])
@login_required
def delete_lead(lead_id):
    service = LeadService()
    lead = service.delete_lead(lead_id)
    if not lead:
        return jsonify({"error": "Lead nao encontrado."}), 404
    return jsonify({"status": "deleted"})


@bp.route("/dashboard", methods=["GET"])
@login_required
def get_dashboard():
    service = DashboardService()
    return jsonify(service.get_dashboard_data())


@bp.route("/reports", methods=["GET"])
@login_required
def get_reports():
    service = ReportService()
    return jsonify(service.get_report_data())
