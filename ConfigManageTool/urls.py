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
    path('rule/list/diff/pdf/<str:compare_key>',
         views.send_mail, name="rule-list-pdf"),
    path('report/download/<str:compare_key>',
         views.download_compare_report, name="report-download"),
]

urlpatterns = [
    path('ConfigManageTool/ruleset/compare/', include(ruleset_comparer_pattern)),
]
