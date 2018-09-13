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
    path('RulesetComparer/page/ruleset/compare/', views.page_compare_select),
    path('RulesetComparer/rule/list/compare/<str:country>/env1/<str:environment1>/env2/<str:environment2>/', views.compare_rule_list),
    path('RulesetComparer/rule/list/<str:environment>/<str:country>/', views.get_rule_list),
    path('RulesetComparer/rule/<str:environment>/<str:country>/<str:rule_set_name>/', views.get_rule_set),
    path('RulesetComparer/compare/<str:country>/env1/<str:environment1>/env2/<str:environment2>/<str:rule_set_name>', views.compare_rule_set),

    path('RulesetComparer/download/git/<str:country>/', views.download_rule_set_from_git),
    path('RulesetComparer/compare/<str:country>', views.compare_country_rule_set),
    path('RulesetComparer/temp_query_compare_ruleset.html', views.download_rule_set_test),
]
