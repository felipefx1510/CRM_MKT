from datetime import datetime

from app.extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30))
    empresa = db.Column(db.String(120))
    origem = db.Column(db.String(80), nullable=False)
    mensagem = db.Column(db.Text)
    segmento = db.Column(db.String(120))
    interesse = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    classificacao_score = db.Column(db.String(20), default="Frio", nullable=False)
    status = db.Column(db.String(40), default="Novo Lead", nullable=False)
    resumo_ia = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    interactions = db.relationship(
        "Interaction",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "empresa": self.empresa,
            "origem": self.origem,
            "mensagem": self.mensagem,
            "segmento": self.segmento,
            "interesse": self.interesse,
            "score": self.score,
            "classificacao_score": self.classificacao_score,
            "status": self.status,
            "resumo_ia": self.resumo_ia,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
