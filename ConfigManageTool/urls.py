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
    path('select/', views.environment_select_page, name="environment-select"),
    path('detail/<str:environment_name>/<str:compare_key>/<str:rule_name>',
         views.rule_detail_page, name="rule-detail"),
    path('diff/<str:compare_key>/<str:rule_name>',
         views.rule_diff_page, name="rule-diff"),
    path('report/mail/<str:compare_key>',
         views.send_mail, name="report-send"),
    path('report/download/<str:compare_key>',
         views.download_compare_report, name="report-download")
]

admin_console_ruleset_pattern = [
    path('', views.admin_console_page),
    path('server_log', views.admin_console_server_log_page, name="server-log"),
    path('server_log/<int:log_type>', views.admin_console_server_log_page, name="server-log-type"),
    path('scheduler/list', views.admin_console_scheduler_list_page, name="task-manager-list"),
    path('scheduler/create', views.admin_console_scheduler_create_page, name="task-create"),
    path('scheduler/update/<int:scheduler_id>', views.admin_console_scheduler_update_page, name="task-update"),

]

admin_console_pattern = [
    path('admin_console/module/list', views.get_module_list),
    path('admin_console/module/create', views.create_module),
]

ruleset_scheduler_pattern = [
    path('<int:scheduler_id>', views.get_scheduler),
    path('list', views.get_scheduler_list),
    path('create', views.create_scheduler, name="create-scheduler"),
    path('update', views.update_scheduler, name="update-scheduler"),
    path('delete', views.delete_scheduler, name="delete-scheduler"),
]

urlpatterns = [
    path('ConfigManageTool/ruleset/compare/', include(ruleset_comparer_pattern)),
    path('ConfigManageTool/ruleset/scheduler/', include(ruleset_scheduler_pattern)),
    path('ConfigManageTool/admin_console/ruleset/', include(admin_console_ruleset_pattern)),
]
