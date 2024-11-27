from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.vpn.models import *
from apps.ticket.models import *

from django.db.models import Count, Q


def convert_date(date):
    date = date.replace(" ", "")
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    return year + month + day


def convert_date2(date):
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return year + "/" + month + "/" + day


def filter_date(date, queryset):
    selected_date_str = date.split("تا")
    if len(selected_date_str) == 2:
        start_date = convert_date(selected_date_str[0])
        end_date = convert_date(selected_date_str[1])
    else:
        start_date = convert_date(selected_date_str[0])
        end_date = start_date

    return queryset.filter(date__range=(start_date, end_date)).order_by('date')


def filter_date_year(date, queryset):
    date = int(date)
    if date == 0:
        return queryset
    start_date = date
    end_date = start_date + 10000

    return queryset.filter(date__gte=start_date, date__lte=end_date).order_by('date')


def filter_vpn(vpn, queryset):
    if vpn == "0":
        return queryset
    return queryset.filter(vpn_id=vpn)


def filter_country_server(country_server, queryset):
    if country_server == "0":
        return queryset
    return queryset.filter(server_country=country_server)


def filter_province(province, queryset):
    return queryset.filter(city=province)


def filter_country(country, queryset):
    if country == "0":
        return queryset
    return queryset.filter(vpn__vpn_country=country)


def filter_operator(oprator, queryset):
    return queryset.filter(oprator__in=oprator)


# Create your views here.
class LandingView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class ReportDashboardsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # محدود کردن داده‌های بازیابی شده
        test = Test.objects.select_related('vpn').only('id', 'date', 'vpn__name', 'status', 'server_isp', 'oprator')

        # آخرین تست‌ها
        last_test = test.order_by('-id')[:12]
        for item in last_test:
            item.date = convert_date2(item.date)
            item.vpn.name2 = item.vpn.name.replace(' ', '')

        # ساخت فیلترها
        filter_dict = {
            item['filter'].replace(" ", "_"): item['count']
            for item in test.values('filter').annotate(count=Count('filter'))
        }

        # VPN
        vpn_data = test.exclude(status="Filter").values('vpn').annotate(count=Count('vpn'))
        best_vpn_id = max(vpn_data, key=lambda x: x['count'], default=None)['vpn'] if vpn_data else None
        best_vpn = Vpn.objects.only('id', 'name').filter(pk=best_vpn_id).first() if best_vpn_id else None

        # ISP و اپراتور
        best_isp = test.values('server_isp').annotate(count=Count('id')).exclude(server_isp=None).order_by(
            '-count').first()
        best_oprator = test.values('oprator').annotate(count=Count('id')).exclude(status="Filter").order_by(
            '-count').first()

        # کشور برتر
        best_country_data = (
            test.exclude(status="Filter")
            .exclude(vpn__vpn_country=None)
            .values('vpn__vpn_country')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        best_country = (
            Country.objects.only('id', 'name').filter(id=best_country_data['vpn__vpn_country']).first()
            if best_country_data
            else None
        )

        # نوتیفیکیشن
        notification_bool = Notification.objects.filter(user=self.request.user, is_read=False).exists()

        # اضافه کردن به context
        context.update({
            "filter": filter_dict,
            "last_test": last_test,
            "best_vpn": best_vpn,
            "best_isp": best_isp,
            "best_oprator": best_oprator,
            "best_country": best_country,
            "notification_bool": notification_bool,
        })

        return context


class LinerChartView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # استفاده از only() برای کاهش مقدار داده‌ها
        vpn = Vpn.objects.only('id', 'vpn_country')  # تنها فیلدهای مورد نیاز را بارگذاری می‌کنیم
        all_test = Test.objects.only('date', 'oprator', 'status', 'city',
                                     'server_country')  # فیلترهای محدودتر برای کاهش بار

        # کشور سرور و استان‌ها فقط برای فیلترها
        country_server_ids = list(all_test.values_list('server_country', flat=True).distinct())
        country_server_ids = [item for item in country_server_ids if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_ids).order_by('persian_name')

        province_ids = list(all_test.values_list('city', flat=True).distinct())
        province_ids = [item for item in province_ids if item != 'nan' and item != 'تهران']

        country_ids = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_ids = [item for item in country_ids if item != 'nan']
        country = Country.objects.filter(id__in=country_ids).order_by('persian_name')

        # دریافت مقادیر فیلتر از URL
        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_province = self.request.GET.get('province')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        # بدون فیلتر
        no_filter = all_test.filter(status='Without Filter').order_by('date')

        # اعمال فیلترها
        if selected_date_str:
            all_test = filter_date(selected_date_str, all_test)
            no_filter = filter_date(selected_date_str, no_filter)

        if selected_vpn:
            no_filter = filter_vpn(selected_vpn, no_filter)
            all_test = filter_vpn(selected_vpn, all_test)

        if selected_country_server:
            no_filter = filter_country_server(selected_country_server, no_filter)
            all_test = filter_country_server(selected_country_server, all_test)

        if selected_country:
            no_filter = filter_country(selected_country, no_filter)
            all_test = filter_country(selected_country, all_test)

        if selected_province:
            no_filter = filter_province(selected_province, no_filter)
            all_test = filter_province(selected_province, all_test)
        else:
            selected_province = "تهران"
            no_filter = filter_province(selected_province, no_filter)
            all_test = filter_province(selected_province, all_test)

        # کاهش زمان با استفاده از groupby و تجمیع داده‌ها به صورت مستقیم
        results = []
        data_dict = {}

        # فیلتر کردن و محاسبه شمارش برای هر اپراتور
        for test in no_filter:
            date = str(test.date)
            date_str = date[:4] + '_' + date[4:6] + '_' + date[6:8]

            if date_str not in data_dict:
                data_dict[date_str] = {
                    'year': date[:4],
                    'month': date[4:6],
                    'day': date[6:8],
                    'irancell': 0,
                    'rightel': 0,
                    'mci': 0,
                    'tci': 0
                }

            # افزایش شمارش اپراتور مربوطه
            operator = test.oprator.lower()
            if operator == 'irancell':
                data_dict[date_str]['irancell'] += 1
            elif operator == 'rightel':
                data_dict[date_str]['rightel'] += 1
            elif operator == 'mci':
                data_dict[date_str]['mci'] += 1
            elif operator == 'tci':
                data_dict[date_str]['tci'] += 1

        # تبدیل دیکشنری به لیست
        results = list(data_dict.values())

        # تعداد اپراتورها بدون فیلتر و با فیلتر
        irancell_no_filter = no_filter.filter(oprator="Irancell").count()
        irancell_filter = all_test.filter(oprator="Irancell").count() - irancell_no_filter

        mci_no_filter = no_filter.filter(oprator="MCI").count()
        mci_filter = all_test.filter(oprator="MCI").count() - mci_no_filter

        rightel_no_filter = no_filter.filter(oprator="RighTel").count()
        rightel_filter = all_test.filter(oprator="RighTel").count() - rightel_no_filter

        tci_no_filter = no_filter.filter(oprator="TCI").count()
        tci_filter = all_test.filter(oprator="TCI").count() - rightel_no_filter

        # افزودن داده‌ها به context
        context['data1'] = results
        context['irancell_no_filter'] = irancell_no_filter
        context['irancell_filter'] = irancell_filter
        context['mci_no_filter'] = mci_no_filter
        context['mci_filter'] = mci_filter
        context['rightel_no_filter'] = rightel_no_filter
        context['rightel_filter'] = rightel_filter
        context['tci_no_filter'] = tci_no_filter
        context['tci_filter'] = tci_filter

        # اطلاعات فیلترها
        context['vpn'] = vpn
        context['province'] = province_ids
        context['country_server'] = country_server
        context['country'] = country

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_vpn'] = selected_vpn
        context['selected_country'] = selected_country
        context['selected_province'] = selected_province

        return context


class VpnCtreatorView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # دریافت تعداد VPN‌ها بر اساس کشور به صورت مستقیم
        vpn_counts_by_country = Vpn.objects.values('vpn_country').annotate(count=Count('vpn_country')).order_by(
            '-count')

        # استخراج شناسه‌های کشورها
        country_ids = [item['vpn_country'] for item in vpn_counts_by_country]

        # واکشی تمام کشورها به صورت یکجا
        countries = Country.objects.filter(id__in=country_ids).only('id', 'name', 'country_id', 'continent',
                                                                    'persian_name')

        # ساخت دیکشنری برای جستجو سریع کشورها بر اساس id
        country_dict = {country.id: country for country in countries}

        # ایجاد لیست داده‌ها بر اساس اطلاعات موجود در country_dict
        country_list = []
        for item in vpn_counts_by_country:
            country_id = item['vpn_country']
            country = country_dict.get(country_id)
            if country:
                data = {
                    "name": country.name,
                    "country_id": country.country_id,
                    "continent": country.continent,
                    "value": item['count'],
                    "persian_name": country.persian_name
                }
                country_list.append(data)

        # اضافه کردن داده‌ها به context
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['country_data'] = country_list
        return context


class IspView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects.exclude(server_isp=None)
        vpn = Vpn.objects.filter()

        country_server_id = list(test.values_list('server_country', flat=True).distinct())
        country_server_id = [item for item in country_server_id if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_id).order_by('persian_name')

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id).order_by('persian_name')

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        if selected_date_str:
            test = filter_date_year(selected_date_str, test)

        if selected_vpn:
            test = filter_vpn(selected_vpn, test)

        if selected_country_server:
            test = filter_country_server(selected_country_server, test)

        if selected_country:
            test = filter_country(selected_country, test)

        main_isp = Isp.objects.filter(pk=self.kwargs['pk'])[0]
        main_isp.name2 = main_isp.name.replace(" ", "")
        test_data = test.values('server_isp', 'server_country__name').annotate(server_count=Count('id')).exclude(
            server_isp='nan')

        # ساخت دیکشنری نهایی
        data = {}
        for item in test_data:
            isp = item['server_isp']
            country_m = item['server_country__name']
            count = item['server_count']

            if isp not in data:
                data[isp] = {}
            data[isp][country_m] = count

        test = test.filter(server_isp=main_isp.name)

        isp_ip = test.values('server_ip').distinct()
        isp_country = test.values('server_country__persian_name').distinct()
        isp_vpn = test.values('vpn__name').distinct()

        count_ip = isp_ip.count()
        count_country = isp_country.count()
        count_vpn = isp_vpn.count()

        context['vpn'] = vpn
        context['country_server'] = country_server
        context['country'] = country
        context['data'] = data
        context['isp'] = main_isp

        context['isp_ip'] = isp_ip
        context['isp_vpn'] = isp_vpn
        context['isp_country'] = isp_country

        context['count_ip'] = count_ip
        context['count_country'] = count_country
        context['count_vpn'] = count_vpn

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_vpn'] = selected_vpn
        context['selected_country'] = selected_country

        return context


class VpnByIdView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # انتخاب VPN با استفاده از pk
        vpn = Vpn.objects.filter(pk=self.kwargs['pk']).only('id', 'name', 'vpn_country').first()

        # دریافت تست‌ها که وضعیت آن‌ها بدون فیلتر است
        tests = Test.objects.filter(vpn_id=vpn.id, status='Without Filter')

        # دریافت کشورهای سرور
        country_server_id = tests.values_list('server_country', flat=True).distinct().exclude(
            server_country__isnull=True)
        country_server = Country.objects.filter(id__in=country_server_id).order_by('persian_name')

        # دریافت کشورهای VPN
        country_id = Vpn.objects.filter(id=self.kwargs['pk']).values_list('vpn_country', flat=True).distinct()
        country = Country.objects.filter(id__in=country_id).order_by('persian_name')

        # فیلتر کردن بر اساس انتخاب‌های کاربر
        selected_date_str = self.request.GET.get('selected_date')
        if selected_date_str:
            tests = filter_date(selected_date_str, tests)

        # فیلتر انتخابی بر اساس کشورهای سرور و کشور
        selected_country_server = self.request.GET.get('server_country', 0)
        selected_country = self.request.GET.get('country', 0)

        # استفاده از distinct برای دریافت لیست‌های منحصر به فرد
        server_ips = list(tests.values_list('server_ip', flat=True).exclude(server_ip__isnull=True).distinct())
        server_ip_count = len(server_ips)

        server_isps = list(tests.values_list('server_isp', flat=True).exclude(server_isp__isnull=True).distinct())
        server_isp_count = len(server_isps)

        server_regions = list(
            tests.values_list('server_region', flat=True).exclude(server_region__isnull=True).distinct())
        server_region_count = len(server_regions)

        server_countries = Country.objects.filter(id__in=tests.values_list('server_country', flat=True).distinct())
        server_country_count = server_countries.count()

        # اصلاح نام VPN در صورت نیاز
        vpn.name2 = vpn.name.replace(' ', '')  # تنها یک بار اصلاح نام انجام می‌شود

        # اضافه کردن اطلاعات به context
        context['vpn'] = vpn
        context['country_server'] = country_server
        context['country'] = country

        context['server_ip_count'] = server_ip_count
        context['server_isp_count'] = server_isp_count
        context['server_region_count'] = server_region_count
        context['server_country_count'] = server_country_count

        context['server_ips'] = server_ips
        context['server_isps'] = server_isps
        context['server_regions'] = server_regions
        context['server_countries'] = server_countries

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_country'] = selected_country

        return context


class OperatorView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects
        vpn = Vpn.objects.filter()

        province = list(test.values_list('city', flat=True).distinct())
        province = [item for item in province if item != 'nan']
        province = [item for item in province if item != 'تهران']

        country_server_id = list(test.values_list('server_country', flat=True).distinct())
        country_server_id = [item for item in country_server_id if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_id).order_by('persian_name')

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id).order_by('persian_name')

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_province = self.request.GET.get('province')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        if selected_date_str:
            test = filter_date(selected_date_str, test)

        if selected_vpn:
            test = filter_vpn(selected_vpn, test)

        if selected_country_server:
            test = filter_country_server(selected_country_server, test)

        if selected_country:
            test = filter_country(selected_country, test)

        if selected_province:
            test = filter_province(selected_province, test)
        else:
            selected_province = "تهران"
            test = filter_province(selected_province, test)

        operators = ["Irancell", "MCI", "RighTel", "TCI"]
        operator_data = {}
        for operator in operators:
            operator_tests = test.filter(oprator=operator, status="Without Filter")
            vpn_count = operator_tests.values('vpn').annotate(count=models.Count('vpn')).order_by('-count')[:7]

            vpn_names = []
            vpn_test_counts = []
            for item in vpn_count:
                vpn_obj = Vpn.objects.get(id=item['vpn'])
                vpn_names.append(vpn_obj.name)
                vpn_test_counts.append(item['count'])

            operator_data[operator] = {
                'vpn_names': vpn_names,
                'vpn_test_counts': vpn_test_counts
            }

        context['country_server'] = country_server
        context['country'] = country
        context['vpn'] = vpn
        context['province'] = province

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_vpn'] = selected_vpn
        context['selected_country'] = selected_country
        context['selected_province'] = selected_province

        context['irancell_names'] = operator_data["Irancell"]['vpn_names']
        context['irancell_count'] = operator_data["Irancell"]['vpn_test_counts']

        context['mci_names'] = operator_data["MCI"]['vpn_names']
        context['mci_count'] = operator_data["MCI"]['vpn_test_counts']

        context['rightel_names'] = operator_data["RighTel"]['vpn_names']
        context['rightel_count'] = operator_data["RighTel"]['vpn_test_counts']

        context['tci_names'] = operator_data["TCI"]['vpn_names']
        context['tci_count'] = operator_data["TCI"]['vpn_test_counts']

        return context


class ProcessView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects.filter()
        vpn = Vpn.objects.filter()

        province = list(test.values_list('city', flat=True).distinct())
        province = [item for item in province if item != 'nan']
        province = [item for item in province if item != 'تهران']

        country_server_id = list(test.values_list('server_country', flat=True).distinct())
        country_server_id = [item for item in country_server_id if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_id).order_by('persian_name')

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id).order_by('persian_name')

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_province = self.request.GET.get('province')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')
        selected_operators = self.request.GET.getlist('operator')

        if selected_date_str:
            test = filter_date(selected_date_str, test)

        if selected_vpn:
            test = filter_vpn(selected_vpn, test)

        if selected_country_server:
            test = filter_country_server(selected_country_server, test)

        if selected_country:
            test = filter_country(selected_country, test)

        if selected_province:
            test = filter_province(selected_province, test)
        else:
            selected_province = "تهران"
            test = filter_province(selected_province, test)

        if selected_operators:
            test = filter_operator(selected_operators, test)
        else:
            selected_operators = ["TCI", "RighTel", "MCI", "Irancell"]
            test = test

        filter = test.values('filter').annotate(count=models.Count('filter'))
        filter_dict = {}
        for item in filter:
            filter_dict[item['filter'].replace(" ", "_")] = item['count']

        filter_vpn_count = test.filter(status="Filter").count()
        no_filter_vpn_count = test.filter(status="Without Filter").count()

        total = no_filter_vpn_count + filter_vpn_count

        if filter_vpn_count == 0:
            filter_vpn_percent = 0
            no_filter_vpn_percent = 100

        elif no_filter_vpn_count == 0:
            filter_vpn_percent = 100
            no_filter_vpn_percent = 0
        else:
            filter_vpn_percent = (filter_vpn_count / total) * 100
            no_filter_vpn_percent = (no_filter_vpn_count / total) * 100

        filter_vpn_percent = round(filter_vpn_percent, 2)
        no_filter_vpn_percent = round(no_filter_vpn_percent, 2)

        server_ips = set(test.values_list('server_ip', flat=True).distinct())
        server_ips = list(server_ips)
        server_ips = [ip for ip in server_ips if ip != 'nan']
        server_ip_count = len(server_ips)

        server_isps = set(test.values_list('server_isp', flat=True).distinct())
        server_isps = list(server_isps)
        server_isps = [ip for ip in server_isps if ip != 'nan']
        server_isp_count = len(server_isps)

        server_regions = set(test.values_list('server_region', flat=True).distinct())
        server_regions = list(server_regions)
        server_regions = [ip for ip in server_regions if ip != 'nan']
        server_region_count = len(server_regions)

        server_countries_id = list(test.values_list('server_country', flat=True).distinct())
        server_countries_id = [ip for ip in server_countries_id if ip != 166]
        server_countries = Country.objects.filter(id__in=server_countries_id)
        server_country_count = len(server_countries)

        context['filter'] = filter_dict
        context['server_ip_count'] = server_ip_count
        context['server_isp_count'] = server_isp_count
        context['server_region_count'] = server_region_count
        context['server_country_count'] = server_country_count
        context['total'] = total

        context['filter_vpn_percent'] = filter_vpn_percent
        context['no_filter_vpn_percent'] = no_filter_vpn_percent
        context['no_filter_vpn_count'] = no_filter_vpn_count
        context['filter_vpn_count'] = filter_vpn_count

        context['vpn'] = vpn
        context['country_server'] = country_server
        context['country'] = country
        context['province'] = province

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_vpn'] = selected_vpn
        context['selected_country'] = selected_country

        context['server_ips'] = server_ips
        context['server_isps'] = server_isps
        context['server_regions'] = server_regions
        context['server_countries'] = server_countries
        context['selected_province'] = selected_province
        context['selected_operators'] = selected_operators

        return context
