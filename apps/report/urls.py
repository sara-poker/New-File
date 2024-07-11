from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "",
        ReportDashboardsView.as_view(template_name="landing.html"),
        name="landing",
    ),
    path(
        "report",
        login_required(ReportDashboardsView.as_view(template_name="dashboard_report.html")),
        name="index",
    ),
    path(
        "report/linerChart",
        login_required(LinerChartView.as_view(template_name="liner_chart.html")),
        name="liner_chart",
    ),
    path(
        "report/vpn-ctreator",
        login_required(VpnCtreatorView.as_view(template_name="vpn_ctreator.html")),
        name="vpn_ctreator",
    ),

    path(
        "report/isp",
        login_required(IspView.as_view(template_name="isp.html")),
        name="isp",
    ),
    path(
        "report/vpn/<int:pk>",
        login_required(VpnByIdView.as_view(template_name="vpn.html")),
        name="vpn_by_id",
    ),
    path(
        "report/Process",
        login_required(ProcessView.as_view(template_name="process.html")),
        name="Process_view",
    ),
    path(
        "report/Operator",
        login_required(OperatorView.as_view(template_name="Operator.html")),
        name="Operator_view",
    ),

]
