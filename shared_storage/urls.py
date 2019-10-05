from django.urls import path

from shared_storage import views
from django.conf.urls import include

app_name = 'shared_storage'

compare_pattern = [
    path('compare/select', views.select_to_compare_page, name="select-to-compare-page"),
    path('compare/select/filter/environment', views.select_to_compare_filter_environment_page,
         name="select-to-compare-filter-environment-page"),
    path('compare/select/filter/folder', views.select_to_compare_filter_folder_page,
         name="select-to-compare-filter-folder-page"),
]

urlpatterns = [
    path('shared_storage/', include(compare_pattern)),
]
