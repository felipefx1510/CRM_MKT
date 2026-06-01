from app.routes.api_routes import bp as api_routes
from app.routes.auth_routes import bp as auth_routes
from app.routes.dashboard_routes import bp as dashboard_routes
from app.routes.lead_routes import bp as lead_routes
from app.routes.pipeline_routes import bp as pipeline_routes
from app.routes.report_routes import bp as report_routes

__all__ = [
    "auth_routes",
    "dashboard_routes",
    "lead_routes",
    "pipeline_routes",
    "report_routes",
    "api_routes",
]
