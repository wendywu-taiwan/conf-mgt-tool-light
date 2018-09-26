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

urlpatterns = [
    path('RulesetComparer/page/ruleset/compare/', views.page_compare_select, name="ruleset-compare"),
    path('RulesetComparer/page/ruleset/compare/list', views.page_compare_rule_list_item, name="ruleset-compare-list"),
    path('RulesetComparer/page/ruleset/compare/detail', views.page_compare_rule_detail,
         name="ruleset-compare-rule-detail"),
    path('RulesetComparer/page/ruleset/compare/diff', views.page_compare_rule_diff,
         name="ruleset-compare-rule-diff"),
path('RulesetComparer/ruleset/compare/detail/<str:country>/<str:env>/<str:rule_set_name>', views.compare_rule_detail,
         name="ruleset-compare-rule-detail"),
]
