from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.ticket.models import *
from django.http import HttpResponse
import pandas as pd
from django.http import JsonResponse
from django.views import View

from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

from apps.vpn.models import *


def convert_month(month):
    if month == "01":
        return "فروردین"
    if month == "02":
        return "اردیبهشت"
    if month == "03":
        return "خرداد"
    if month == "04":
        return "تیر"
    if month == "05":
        return "مرداد"
    if month == "06":
        return "شهریور"
    if month == "07":
        return "مهر"
    if month == "08":
        return "آبان"
    if month == "09":
        return "آذر"
    if month == "10":
        return "دی"
    if month == "11":
        return "بهمن"
    if month == "12":
        return "اسفند"


def convert_date(date):
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return year + "/" + month + "/" + day


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


class StaffRequiredMixin3(AccessMixin):
    redirect_url = '/report'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class DownloadDataView(TemplateView):
    template_name = "download_data.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["province"] = Test.objects.values_list('city', flat=True).distinct()
        return context

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET:
            return self.export_excel(request)
        return super().get(request, *args, **kwargs)

    def export_excel(self, request):
        selected_startDate = request.GET.get('startDate')
        selected_endDate = request.GET.get('endDate')
        selected_province = request.GET.get('province')
        selected_operator = request.GET.get('operator')

        if not all([selected_startDate, selected_endDate, selected_province, selected_operator]):
            return HttpResponse("لطفاً همه فیلترها را وارد کنید!", status=400)

        tests = Test.objects.filter(date__range=(selected_startDate, selected_endDate), city=selected_province)
        if selected_operator != "all":
            tests = tests.filter(oprator=selected_operator)

        data = [
            {
                "Date": test.date,
                "Date2": convert_date(test.date),
                "Year": int(str(test.date)[:4]),
                "Month1": int(str(test.date)[4:6]),
                "Month2": convert_month(str(test.date)[4:6]),
                "Day": int(str(test.date)[6:8]),
                "DaysOfTheWeek": None,
                "clock": test.time,
                "Event": test.city,
                "Holiday": None,
                "SecuretyEvent": None,
                "VPN Name": test.vpn.name if test.vpn else None,
                "Internet Provider": test.oprator,
                "Platform": test.vpn.platform if test.vpn else None,
                "Filter": test.status,
                "Filter status": test.filter,
                "ServerIP": test.server_ip,
                "ServerHost": test.server_host,
                "ServerISP": None,
                "ServerCountry": test.server_country.name if test.server_country else None,
                "ServerRegion": test.server_region,
                "ServerCity": test.server_city,
                "ServerLatitude": test.server_Latitude,
                "ServerLongitude": test.server_Longitude,
                "TestNumberOnDey": None,
                "PingSpeed": test.ping_speed,
                "TTL": test.ttl,
                "NumberOfTest": None,
                "vpn maker": test.vpn.vpn_maker if test.vpn else None,
                "vpn Country": test.vpn.vpn_country.name if test.vpn and test.vpn.vpn_country else None,
                "vpn normal user fee":None,
                "Proxy Port": test.proxy_port,
                "Proxy Secret": test.proxy_secret,
            }
            for test in tests
        ]

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=filtered_data.xlsx'
        df.to_excel(response, index=False)

        return response


class DeleteDataView(StaffRequiredMixin3, TemplateView):
    template_name = "delete_data.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects.filter()
        province = list(test.values_list('city', flat=True).distinct())
        context['province'] = province

        selected_startDate = self.request.GET.get('startDate')
        selected_endDate = self.request.GET.get('endDate')
        selected_province = self.request.GET.get('province')
        selected_operator = self.request.GET.get('operator')

        if not selected_startDate:
            context['success'] = False
            context['msg'] = "لطفا شروع بازه تاریخ را وارد کنید!"
            return context

        if not selected_endDate:
            context['success'] = False
            context['msg'] = "لطفا پایان  بازه تاریخ را وارد کنید!"
            return context

        if not selected_province:
            context['success'] = False
            context['msg'] = "لطفا استان مورد نظر را وارد کنید!"
            return context

        if not selected_operator:
            context['success'] = False
            context['msg'] = "لطفا اپراتور مورد نظر را وارد کنید!"
            return context

        test = test.filter(date__range=(selected_startDate, selected_endDate))
        if selected_operator != "all":
            test = test.filter(oprator=selected_operator)
        test = test.filter(city=selected_province)

        deleted_count, _ = test.delete()

        context['success'] = True
        context['msg'] = f" رکورد با موفقیت حذف شد."
        return context


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


class NotificationView(TemplateView):
    def get_context_data(self, **kwargs):
        # دریافت context اصلی
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # دریافت تمام اعلان‌های کاربر فعلی
        notifications = Notification.objects.filter(user=self.request.user).order_by('-created_at')

        # اضافه کردن اعلان‌ها به context
        context['notifications'] = notifications
        return context


class UpdateNotificationStatusView(View):
    def post(self, request, *args, **kwargs):
        # بروزرسانی وضعیت اعلان‌ها برای کاربر فعلی
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
