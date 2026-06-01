from flask import current_app

from app.agents.followup_agent import FollowupAgent
from app.agents.summary_agent import SummaryAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.repositories.lead_repository import LeadRepository
from app.services.ollama_service import OllamaService


class SupervisorService:
    def __init__(self):
        self.lead_repository = LeadRepository()
        self.ollama = OllamaService(
            base_url=current_app.config["OLLAMA_URL"],
            model=current_app.config["OLLAMA_MODEL"],
            timeout=current_app.config["OLLAMA_TIMEOUT"],
        )
        self.summary_agent = SummaryAgent(self.ollama)
        self.followup_agent = FollowupAgent(self.ollama)
        self.supervisor_agent = SupervisorAgent(
            ollama_service=self.ollama,
            lead_repository=self.lead_repository,
            summary_agent=self.summary_agent,
            followup_agent=self.followup_agent,
        )

    def run(self, user_message):
        return self.supervisor_agent.run(user_message)
