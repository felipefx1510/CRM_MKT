from app.extensions import db
from app.models.lead import Lead


class DashboardService:
    def get_dashboard_data(self):
        total_leads = Lead.query.count()
        leads_quentes = Lead.query.filter_by(classificacao_score="Quente").count()
        leads_em_negociacao = Lead.query.filter_by(status="Negociacao").count()
        conversoes = Lead.query.filter_by(status="Fechado").count()
        taxa_conversao = (
            round((conversoes / total_leads) * 100, 2) if total_leads else 0
        )

        charts = {
            "leads_por_origem": self._leads_por_origem(),
            "leads_por_mes": self._leads_por_mes(),
            "conversoes_por_canal": self._conversoes_por_canal(),
            "scores_distribuicao": self._scores_distribuicao(),
            "evolucao_leads": self._leads_por_mes(),
        }

        return {
            "kpis": {
                "total_leads": total_leads,
                "leads_quentes": leads_quentes,
                "leads_em_negociacao": leads_em_negociacao,
                "conversoes": conversoes,
                "taxa_conversao": taxa_conversao,
            },
            "charts": charts,
        }

    def _leads_por_origem(self):
        results = (
            db.session.query(Lead.origem, db.func.count(Lead.id))
            .group_by(Lead.origem)
            .all()
        )
        labels = [row[0] for row in results]
        values = [row[1] for row in results]
        return {"labels": labels, "values": values}

    def _leads_por_mes(self):
        results = (
            db.session.query(
                db.func.date_trunc("month", Lead.created_at).label("mes"),
                db.func.count(Lead.id),
            )
            .group_by("mes")
            .order_by("mes")
            .all()
        )
        labels = [row[0].strftime("%Y-%m") for row in results]
        values = [row[1] for row in results]
        return {"labels": labels, "values": values}

    def _conversoes_por_canal(self):
        results = (
            db.session.query(Lead.origem, db.func.count(Lead.id))
            .filter(Lead.status == "Fechado")
            .group_by(Lead.origem)
            .all()
        )
        labels = [row[0] for row in results]
        values = [row[1] for row in results]
        return {"labels": labels, "values": values}

    def _scores_distribuicao(self):
        results = (
            db.session.query(Lead.classificacao_score, db.func.count(Lead.id))
            .group_by(Lead.classificacao_score)
            .all()
        )
        labels = [row[0] for row in results]
        values = [row[1] for row in results]
        return {"labels": labels, "values": values}
