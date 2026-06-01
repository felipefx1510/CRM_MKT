from datetime import datetime

from app.extensions import db


class Interaction(db.Model):
    __tablename__ = "interactions"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    lead = db.relationship("Lead", back_populates="interactions")

    def to_dict(self):
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "mensagem": self.mensagem,
            "tipo": self.tipo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
