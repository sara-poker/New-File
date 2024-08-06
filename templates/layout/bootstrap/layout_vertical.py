from django.conf import settings
import json

from web_project.template_helpers.theme import TemplateHelper

menu_file_path = settings.BASE_DIR / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / "vertical_menu.json"
# menu_file_path2 = settings.BASE_DIR / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / "vertical_menu2.json"

menu_file = {
    "menu": [
        {
            "name": "صفحات",
            "icon": "menu-icon tf-icons ti ti-smart-home",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "index",
                    "name": "نمای کلی",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "liner_chart",
                    "name": "روند نگاری",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "/report/vpn/1",
                    "external": True,
                    "name": "شناسنامه ابزار گریز",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "vpn_ctreator",
                    "name": "سازندگان ابزار گریز",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "isp",
                    "name": "ارائه دهندگان خدمات اینترنتی",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "Process_view",
                    "name": "روند مسدود سازی",
                    "slug": "process_view"
                },
                {
                    "url": "Operator_view",
                    "name": "پر اتصال ترین",
                    "slug": "Operator_view"
                },

            ]
        },
{
            "name": "پشتیبانی",
            "icon": "menu-icon tf-icons ti ti-help",
            "slug": "support",
            "submenu":[
                {
                    "url": "all_ticket",
                    "name": "تیکت ها",
                    "slug": "all_ticket"
                },
            ]
        }
    ]
}

menu_file2 = {
    "menu": [
        {
            "name": "صفحات",
            "icon": "menu-icon tf-icons ti ti-smart-home",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "index",
                    "name": "نمای کلی",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "liner_chart",
                    "name": "روند نگاری",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "/report/vpn/1",
                    "external": True,
                    "name": "شناسنامه ابزار گریز",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "vpn_ctreator",
                    "name": "سازندگان ابزار گریز",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "isp",
                    "name": "ارائه دهندگان خدمات اینترنتی",
                    "slug": "dashboard-analytics"
                },
                {
                    "url": "Process_view",
                    "name": "روند مسدود سازی",
                    "slug": "process_view"
                },
                {
                    "url": "Operator_view",
                    "name": "پر اتصال ترین",
                    "slug": "Operator_view"
                }

            ]
        },
        {
            "name": "پشتیبانی",
            "icon": "menu-icon tf-icons ti ti-help",
            "slug": "support",
            "submenu":[
                {
                    "url": "all_ticket",
                    "name": "تیکت ها",
                    "slug": "all_ticket"
                },
            ]
        }
    ]
}

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON
        menu_data = json.load(menu_file_path.open()) if menu_file_path.exists() else []
        menu_data2 = menu_file
        menu_data3 = menu_file2

        # Updated context with menu_data
        context.update({"menu_data": menu_data,
                        "menu_data2": menu_data2,
                        "menu_data3": menu_data3})
