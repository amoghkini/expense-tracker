from dashboard import dashboard
from dashboard.views import (
    DashboardView,
)


routes = [
    (
        (dashboard),
            ('/dashboard', 'dashboard_api', DashboardView),
    )
]