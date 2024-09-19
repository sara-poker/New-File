from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path(
        "ticket",
        login_required(SupportView.as_view(template_name="all_ticket.html")),
        name="all_ticket",
    ),
    path(
        "ticket/<int:pk>",
        login_required(SupportViewById.as_view(template_name="all_ticket_id.html")),
        name="ticket",
    ),
    path(
        "ticket/support",
        login_required(UserView.as_view(template_name="support.html")),
        name="support",
    ),
    path(
        "notification",
        login_required(NotificationView.as_view(template_name="notification.html")),
        name="notification",
    ),
    path('notification/update-status',
         login_required(UpdateNotificationStatusView.as_view()),
         name='update_notification_status')
]
