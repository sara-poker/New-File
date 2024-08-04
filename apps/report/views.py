from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.vpn.models import *

from django.db.models import Count
import random


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

    return queryset.filter(date__gte=start_date, date__lte=end_date).order_by('date')


def filter_date_year(date, queryset):
    print("hello mosi py")
    date = int(date)
    if date == 0:
        return queryset
    start_date = date
    end_date = start_date + 10000

    print("start_date>", start_date)
    print("end_date>", end_date)

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
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects.filter()
        last_test = test.order_by('-id')[:12]
        for item in last_test:
            item.date = convert_date2(item.date)
            # item.time = item.time[:5]

        filter = test.values('filter').annotate(count=models.Count('filter'))
        filter_dict = {}
        for item in filter:
            filter_dict[item['filter'].replace(" ", "_")] = item['count']

        vpn = test.exclude(status="Filter").values('vpn').annotate(count=models.Count('vpn'))
        vpn_dict = {}
        for item in vpn:
            vpn_dict[item['vpn']] = item['count']

        best_vpn_id = max(vpn_dict, key=vpn_dict.get)
        best_vpn = Vpn.objects.filter(pk=best_vpn_id).first()
        best_isp = test.values('server_isp').annotate(count=Count('id')).exclude(server_isp='nan').order_by(
            '-count').first()

        best_oprator = test.values('oprator').annotate(count=Count('id')).exclude(status="Filter").order_by(
            '-count').first()

        test = test.exclude(vpn__vpn_country=None)
        best_country_id = test.values('vpn__vpn_country').annotate(count=Count('id')).exclude(
            status="Filter").order_by(
            '-count')[1]


        print(">",best_country_id)
        best_country = Country.objects.get(id=best_country_id['vpn__vpn_country'])

        for item in last_test:
            original_name = item.vpn.name
            modified_name = original_name.replace(' ', '')
            item.vpn.name2 = modified_name

        context['filter'] = filter_dict
        context['last_test'] = last_test

        context['best_vpn'] = best_vpn
        context['best_isp'] = best_isp
        context['best_oprator'] = best_oprator
        context['best_country'] = best_country

        return context


class LinerChartView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        vpn = Vpn.objects.filter()
        all_test = Test.objects.filter()
        country_server_id = list(all_test.values_list('server_country', flat=True).distinct())
        country_server_id = [item for item in country_server_id if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_id)

        province = list(all_test.values_list('city', flat=True).distinct())
        province = [item for item in province if item != 'nan']
        province = [item for item in province if item != 'تهران']

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id)

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_province = self.request.GET.get('province')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        no_filter = all_test.filter(status='Without Filter').order_by('date')

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

        # hello
        results = []
        data_dict = {}
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
                    "tci": 0
                }

            # افزایش شمارش اپراتور مربوطه
            if test.oprator.lower() == 'Irancell'.lower():
                data_dict[date_str]['irancell'] += 1
            elif test.oprator.lower() == 'RighTel'.lower():
                data_dict[date_str]['rightel'] += 1
            elif test.oprator.lower() == 'MCI'.lower():
                data_dict[date_str]['mci'] += 1
            elif test.oprator.lower() == 'TCI'.lower():
                data_dict[date_str]['tci'] += 1

        # تبدیل دیکشنری به لیست
        results = list(data_dict.values())

        irancell_no_filter = no_filter.filter(oprator="Irancell").count()
        irancell_filter = all_test.filter(oprator="Irancell").count() - irancell_no_filter

        mci_no_filter = no_filter.filter(oprator="MCI").count()
        mci_filter = all_test.filter(oprator="MCI").count() - mci_no_filter

        rightel_no_filter = no_filter.filter(oprator="RighTel").count()
        rightel_filter = all_test.filter(oprator="RighTel").count() - rightel_no_filter

        tci_no_filter = no_filter.filter(oprator="TCI").count()
        tci_filter = all_test.filter(oprator="TCI").count() - rightel_no_filter

        context['data1'] = results

        context['irancell_no_filter'] = irancell_no_filter
        context['irancell_filter'] = irancell_filter

        context['mci_no_filter'] = mci_no_filter
        context['mci_filter'] = mci_filter

        context['rightel_no_filter'] = rightel_no_filter
        context['rightel_filter'] = rightel_filter

        context['tci_no_filter'] = tci_no_filter
        context['tci_filter'] = tci_filter

        context['vpn'] = vpn
        context['province'] = province
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
        vpn_counts_by_country = Vpn.objects.values('vpn_country').annotate(count=Count('vpn_country')).order_by(
            '-count')
        print(vpn_counts_by_country)
        data_country = list(vpn_counts_by_country)
        country_list = []
        for item in data_country:
            country = Country.objects.filter(id=item['vpn_country'])
            if country:
                data = {
                    "name": country[0].name,
                    "country_id": country[0].country_id,
                    "continent": country[0].continent,
                    "value": item['count'],
                    "persian_name": country[0].persian_name
                }
                country_list.append(data)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['country_data'] = country_list
        return context


class IspView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        test = Test.objects
        vpn = Vpn.objects.filter()

        country_server_id = list(test.values_list('server_country', flat=True).distinct())
        country_server_id = [item for item in country_server_id if item != 'nan']
        country_server = Country.objects.filter(id__in=country_server_id)

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id)

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        if selected_date_str:
            test = filter_date_year(selected_date_str, test)

        print("count>>", test.count())

        if selected_vpn:
            test = filter_vpn(selected_vpn, test)

        if selected_country_server:
            test = filter_country_server(selected_country_server, test)

        if selected_country:
            test = filter_country(selected_country, test)

        isp = list(test.values_list('server_isp', flat=True).distinct())
        isp = [item for item in isp if item != 'nan']
        isp_list = Isp.objects.filter(name__in=isp)

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

        context['vpn'] = vpn
        context['country_server'] = country_server
        context['country'] = country
        context['data'] = data

        context['selected_date'] = selected_date_str
        context['selected_country_server'] = selected_country_server
        context['selected_vpn'] = selected_vpn
        context['selected_country'] = selected_country

        return context


class VpnByIdView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        vpn = Vpn.objects.filter(pk=self.kwargs['pk'])
        tests = Test.objects.filter(vpn_id=vpn[0].id, status='Without Filter')

        selected_date_str = self.request.GET.get('selected_date')

        if selected_date_str:
            tests = filter_date(selected_date_str, tests)

        server_ips = set(tests.values_list('server_ip', flat=True).distinct())
        server_ips = list(server_ips)
        server_ips = [ip for ip in server_ips if ip != 'nan']
        server_ip_count = len(server_ips)

        server_isps = set(tests.values_list('server_isp', flat=True).distinct())
        server_isps = list(server_isps)
        server_isps = [ip for ip in server_isps if ip != 'nan']
        server_isp_count = len(server_isps)

        server_regions = set(tests.values_list('server_region', flat=True).distinct())
        server_regions = list(server_regions)
        server_regions = [ip for ip in server_regions if ip != 'nan']
        server_region_count = len(server_regions)

        server_countries_id = list(tests.values_list('server_country', flat=True).distinct())
        server_countries_id = [ip for ip in server_countries_id if ip != 166]
        server_countries = Country.objects.filter(id__in=server_countries_id)
        server_country_count = len(server_countries)

        for item in vpn:
            original_name = item.name
            modified_name = original_name.replace(' ', '')
            item.name2 = modified_name

        context['vpn'] = vpn[0]
        context['server_ip_count'] = server_ip_count
        context['server_isp_count'] = server_isp_count
        context['server_region_count'] = server_region_count
        context['server_country_count'] = server_country_count

        context['server_ips'] = server_ips
        context['server_isps'] = server_isps
        context['server_regions'] = server_regions
        context['server_countries'] = server_countries

        context['selected_date'] = selected_date_str

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
        country_server = Country.objects.filter(id__in=country_server_id)

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id)

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
        country_server = Country.objects.filter(id__in=country_server_id)

        country_id = list(vpn.values_list('vpn_country', flat=True).distinct())
        country_id = [item for item in country_id if item != 'nan']
        country = Country.objects.filter(id__in=country_id)

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
            selected_operators = ["TCI","RighTel","MCI","Irancell"]
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
