from .auth.loginAPI import auth_bp
from .admin.adminAPI import admin_bp
from .customer.customerAPI import customer_bp
from .professional.professionalAPI import professional_bp
from .service.serviceAPI import service_bp
from .search.searchAPI import search_bp
from .reports.reportsAPI import reports_bp

api_blueprints = [
    auth_bp,
    admin_bp,
    customer_bp,
    professional_bp,
    service_bp,
    search_bp,
    reports_bp
]
