from app.extensions import db
from app.models.lead import Lead


class ReportService:
    def get_report_data(self):
        total = Lead.query.count()
        media_score = db.session.query(db.func.avg(Lead.score)).scalar() or 0
        maiores_scores = (
            Lead.query.order_by(Lead.score.desc()).limit(5).all()
        )

        por_segmento = (
            db.session.query(Lead.segmento, db.func.count(Lead.id))
            .group_by(Lead.segmento)
            .order_by(db.func.count(Lead.id).desc())
            .all()
        )

        return {
            "total": total,
            "media_score": round(float(media_score), 2),
            "top_scores": [lead.to_dict() for lead in maiores_scores],
            "por_segmento": [
                {"segmento": row[0] or "Nao informado", "total": row[1]}
                for row in por_segmento
            ],
        }
