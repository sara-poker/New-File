from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.ticket.models import *

from django.db.models import Count

from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class StaffRequiredMixin(AccessMixin):
    redirect_url = '/ticket/support'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin2(AccessMixin):
    redirect_url = '/ticket'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class SupportView(StaffRequiredMixin, TemplateView):
    template_name = "all_ticket.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        all_users = User.objects.filter(is_staff=False)

        context['users'] = all_users
        return context


class SupportViewById(StaffRequiredMixin, TemplateView):
    template_name = "support_by_id.html"  # نام فایل قالب خود را تنظیم کنید

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        all_users = User.objects.filter(is_staff=False)
        my_info = all_users.filter(pk=self.kwargs['pk'])

        messages = Message.objects.filter(user=self.kwargs['pk'])

        context['users'] = all_users
        context['my_info'] = my_info[0]
        context['messages'] = messages
        return context

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text')
        user_id = self.kwargs['pk']

        if text:
            Message.objects.create(
                text=text,
                user_id=user_id,
                support_send=True,
                seen=False,
            )

        return redirect(request.path)


class UserView(StaffRequiredMixin2, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        messages = Message.objects.filter(user=self.request.user)

        context['messages'] = messages
        return context

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text')
        user_id = self.request.user.id

        if text:
            Message.objects.create(
                text=text,
                user_id=user_id,
                support_send=False,
                seen=False,
            )

        return redirect(request.path)
