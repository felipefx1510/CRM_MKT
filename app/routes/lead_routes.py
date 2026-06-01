from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required

from app.constants import LEAD_ORIGINS, LEAD_STATUSES
from app.forms import InteractionForm, LeadForm
from app.services.interaction_service import InteractionService
from app.services.lead_service import LeadService

bp = Blueprint("leads", __name__)


@bp.route("/leads")
@login_required
def list_leads():
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
        per_page=10,
    )
    return render_template(
        "leads/list.html",
        pagination=pagination,
        leads=pagination.items,
        search=search,
        status=status,
        origem=origem,
        lead_statuses=LEAD_STATUSES,
        lead_origins=LEAD_ORIGINS,
    )


@bp.route("/leads/new", methods=["GET", "POST"])
@login_required
def create_lead():
    form = LeadForm()
    if request.method == "GET":
        form.status.data = "Novo Lead"
    if form.validate_on_submit():
        service = LeadService()
        service.create_lead(_form_to_data(form))
        flash("Lead cadastrado com sucesso.", "success")
        return redirect(url_for("leads.list_leads"))
    return render_template("leads/form.html", form=form, mode="create")


@bp.route("/leads/<int:lead_id>", methods=["GET"])
@login_required
def lead_detail(lead_id):
    service = LeadService()
    lead = service.get_lead(lead_id)
    if not lead:
        flash("Lead nao encontrado.", "warning")
        return redirect(url_for("leads.list_leads"))

    interaction_service = InteractionService()
    interactions = interaction_service.list_by_lead(lead_id)
    followup_message = session.pop("followup_message", None)
    form = InteractionForm()

    return render_template(
        "leads/detail.html",
        lead=lead,
        interactions=interactions,
        interaction_form=form,
        followup_message=followup_message,
    )


@bp.route("/leads/<int:lead_id>/edit", methods=["GET", "POST"])
@login_required
def edit_lead(lead_id):
    service = LeadService()
    lead = service.get_lead(lead_id)
    if not lead:
        flash("Lead nao encontrado.", "warning")
        return redirect(url_for("leads.list_leads"))

    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        service.update_lead(lead_id, _form_to_data(form))
        flash("Lead atualizado.", "success")
        return redirect(url_for("leads.lead_detail", lead_id=lead_id))

    return render_template("leads/form.html", form=form, mode="edit")


@bp.route("/leads/<int:lead_id>/interactions", methods=["POST"])
@login_required
def add_interaction(lead_id):
    form = InteractionForm()
    if form.validate_on_submit():
        service = InteractionService()
        service.create(
            lead_id,
            {"tipo": form.tipo.data, "mensagem": form.mensagem.data},
        )
        flash("Interacao adicionada.", "success")
    else:
        flash("Dados da interacao invalidos.", "danger")
    return redirect(url_for("leads.lead_detail", lead_id=lead_id))


@bp.route("/leads/<int:lead_id>/summary", methods=["POST"])
@login_required
def generate_summary(lead_id):
    service = LeadService()
    lead = service.get_lead(lead_id)
    if not lead:
        flash("Lead nao encontrado.", "warning")
        return redirect(url_for("leads.list_leads"))

    resumo = service.generate_summary(lead)
    if resumo:
        service.update_lead(lead_id, {"resumo_ia": resumo})
        flash("Resumo IA gerado.", "success")
    else:
        flash("Falha ao gerar resumo IA.", "danger")
    return redirect(url_for("leads.lead_detail", lead_id=lead_id))


@bp.route("/leads/<int:lead_id>/followup", methods=["POST"])
@login_required
def generate_followup(lead_id):
    variation = request.form.get("variacao")
    service = LeadService()
    lead = service.get_lead(lead_id)
    if not lead:
        flash("Lead nao encontrado.", "warning")
        return redirect(url_for("leads.list_leads"))

    mensagem = service.generate_followup(lead, variation=variation)
    if mensagem:
        session["followup_message"] = mensagem
        flash("Follow-up gerado.", "success")
    else:
        flash("Falha ao gerar follow-up.", "danger")
    return redirect(url_for("leads.lead_detail", lead_id=lead_id))


def _form_to_data(form):
    return {
        "nome": form.nome.data,
        "email": form.email.data,
        "telefone": form.telefone.data,
        "empresa": form.empresa.data,
        "origem": form.origem.data,
        "mensagem": form.mensagem.data,
        "segmento": form.segmento.data,
        "interesse": form.interesse.data,
        "status": form.status.data,
    }
