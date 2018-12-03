"""ConfigManageTool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from RulesetComparer import views
from django.conf.urls import url, include

ruleset_comparer_pattern = [
    path('select/', views.environment_select, name="environment-select"),
    path('detail/<str:environment_name>/<str:compare_key>/<str:rule_name>',
         views.rule_detail, name="rule-detail"),
    path('diff/<str:compare_key>/<str:rule_name>',
         views.rule_diff, name="rule-diff"),
    path('report/mail/<str:compare_key>',
         views.send_mail, name="report-send"),
    path('report/download/<str:compare_key>',
         views.download_compare_report, name="report-download"),
    path('test', views.test_page),
]

admin_console_pattern = [
    path('admin_console/module/list', views.get_module_list),
    path('admin_console/module/create', views.create_module),
    path('admin_console/ruleset', views.admin_console),
    path('admin_console/ruleset/server_log/', views.admin_console_server_log),
    path('admin_console/ruleset/server_log/<int:log_type>', views.admin_console_server_log, name="server-log"),
]

scheduler_pattern = [
    path('create', views.create_scheduler_report_task),
    path('update', views.update_scheduler_report_task),
    path('list', views.get_scheduler_report_task_list),
]

urlpatterns = [
    path('ConfigManageTool/ruleset/compare/', include(ruleset_comparer_pattern)),
    path('ConfigManageTool/', include(admin_console_pattern)),
    path('ConfigManageTool/scheduler/report/', include(scheduler_pattern)),

]
