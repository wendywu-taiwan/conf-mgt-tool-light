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
    path('RulesetComparer/download/rulesets/<str:environment>/<str:country>/', views.download_rule_set),
    path('RulesetComparer/download/ruleset/<str:environment>/<str:country>/<str:rule_set_name>/', views.download_single_rule_set),
    path('RulesetComparer/download/git/<str:country>/', views.download_rule_set_from_git),
    path('RulesetComparer/compare/<str:country>', views.compare_country_rule_set),
]
