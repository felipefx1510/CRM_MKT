from app.models.interaction import Interaction
from app.repositories.interaction_repository import InteractionRepository


class InteractionService:
    def __init__(self):
        self.repository = InteractionRepository()

    def list_by_lead(self, lead_id):
        return self.repository.list_by_lead(lead_id)

    def create(self, lead_id, data):
        interaction = Interaction(lead_id=lead_id, **data)
        return self.repository.create(interaction)
