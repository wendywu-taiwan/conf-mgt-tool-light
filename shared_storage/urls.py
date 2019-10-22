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
    path('compare/result/<str:root_key>', views.select_to_compare_result_page,
         name="select-to-compare-result-page"),
    path('compare/file/diff/<str:root_key>/<str:node_key>/<str:type>', views.select_to_compare_file_diff_page,
         name="select-to-compare-file-diff-page"),
    path('compare/file/detail/<str:side>/<str:root_key>/<str:node_key>/<str:diff_result>/<str:file_type>',
         views.select_to_compare_file_detail_page, name="select-to-compare-file-detail-page"),
    path('compare/mail', views.send_compare_result_mail),
]

urlpatterns = [
    path('shared_storage/', include(compare_pattern)),
]
