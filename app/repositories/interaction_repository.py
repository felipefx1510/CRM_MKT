from app.extensions import db
from app.models.interaction import Interaction


class InteractionRepository:
    def list_by_lead(self, lead_id):
        return (
            Interaction.query.filter_by(lead_id=lead_id)
            .order_by(Interaction.created_at.desc())
            .all()
        )

    def create(self, interaction):
        db.session.add(interaction)
        db.session.commit()
        return interaction
