from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path(
        "ticket",
        login_required(SupportView.as_view(template_name="dashboard_report.html")),
        name="all_ticket",
    ),
    path(
        "ticket/<int:pk>",
        login_required(SupportViewById.as_view(template_name="dashboard_report.html")),
        name="ticket",
    ),
    path(
        "ticket/support",
        login_required(UserView.as_view(template_name="dashboard_report.html")),
        name="support",
    )

]