from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.ticket.models import *

from django.db.models import Count


class SupportView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        all_users = User.objects.filter(is_staff=False)

        context['users'] = all_users
        return context


class SupportViewById(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        all_users = User.objects.filter(is_staff=False)
        my_info = all_users.filter(pk=self.kwargs['pk'])

        messages = Message.objects.filter(user=self.kwargs['pk'])

        context['users'] = all_users
        context['my_info'] = my_info[0]
        context['messages'] = messages
        return context


class UserView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
