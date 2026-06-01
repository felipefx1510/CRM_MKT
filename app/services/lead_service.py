from flask import current_app

from app.agents.followup_agent import FollowupAgent
from app.agents.summary_agent import SummaryAgent
from app.constants import LEAD_STATUSES
from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.services.lead_scoring_service import LeadScoringService
from app.services.ollama_service import OllamaService


class LeadService:
    def __init__(self):
        self.lead_repository = LeadRepository()
        self.scoring_service = LeadScoringService()

    def list_paginated(self, search, status, origem, page, per_page):
        query = self.lead_repository.list_filtered(search, status, origem)
        return self.lead_repository.paginate(query, page, per_page)

    def list_by_status(self):
        leads = Lead.query.order_by(Lead.created_at.desc()).all()
        grouped = {status: [] for status in LEAD_STATUSES}
        for lead in leads:
            grouped.setdefault(lead.status, []).append(lead)
        return grouped

    def get_lead(self, lead_id):
        return self.lead_repository.get_by_id(lead_id)

    def create_lead(self, data):
        score, classificacao = self._calculate_score(data)
        data["score"] = score
        data["classificacao_score"] = classificacao
        data.setdefault("status", "Novo Lead")
        lead = Lead(**data)
        return self.lead_repository.create(lead)

    def update_lead(self, lead_id, data):
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            return None
        score, classificacao = self._calculate_score({
            "origem": data.get("origem", lead.origem),
            "interesse": data.get("interesse", lead.interesse),
        })
        data.setdefault("score", score)
        data.setdefault("classificacao_score", classificacao)
        return self.lead_repository.update(lead, data)

    def delete_lead(self, lead_id):
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            return None
        self.lead_repository.delete(lead)
        return lead

    def generate_summary(self, lead):
        summary_agent, _ = self._build_agents()
        return summary_agent.run(lead)

    def generate_followup(self, lead, variation=None, extra_instruction=None):
        _, followup_agent = self._build_agents()
        return followup_agent.run(lead, variation, extra_instruction)

    def _calculate_score(self, data):
        score = self.scoring_service.calculate_score(
            data.get("origem"),
            data.get("interesse"),
        )
        classificacao = self.scoring_service.classify(score)
        return score, classificacao

    def _build_agents(self):
        ollama = OllamaService(
            base_url=current_app.config["OLLAMA_URL"],
            model=current_app.config["OLLAMA_MODEL"],
            timeout=current_app.config["OLLAMA_TIMEOUT"],
        )
        return SummaryAgent(ollama), FollowupAgent(ollama)
