from sqlalchemy import or_

from app.extensions import db
from app.models.lead import Lead


class LeadRepository:
    def get_by_id(self, lead_id):
        return Lead.query.get(lead_id)

    def list_filtered(self, search=None, status=None, origem=None):
        query = Lead.query
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    Lead.nome.ilike(like),
                    Lead.email.ilike(like),
                    Lead.empresa.ilike(like),
                )
            )
        if status:
            query = query.filter(Lead.status == status)
        if origem:
            query = query.filter(Lead.origem == origem)
        return query.order_by(Lead.created_at.desc())

    def paginate(self, query, page, per_page):
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def create(self, lead):
        db.session.add(lead)
        db.session.commit()
        return lead

    def update(self, lead, data):
        for key, value in data.items():
            setattr(lead, key, value)
        db.session.commit()
        return lead

    def delete(self, lead):
        db.session.delete(lead)
        db.session.commit()
