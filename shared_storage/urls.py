from django.urls import path

from shared_storage import views
from django.conf.urls import include

app_name = 'shared_storage'

compare_pattern = [
    path('select', views.select_to_compare_page, name="select-to-compare-page"),
    path('result/<str:root_key>', views.select_to_compare_result_page,
         name="select-to-compare-result-page"),
    path('file/diff/<str:root_key>/<str:node_key>/<str:type>', views.select_to_compare_file_diff_page,
         name="select-to-compare-file-diff-page"),
    path('file/detail/<str:side>/<str:root_key>/<str:node_key>/<str:diff_result>/<str:file_type>',
         views.select_to_compare_file_detail_page, name="select-to-compare-file-detail-page"),
    path('mail', views.send_compare_result_mail),
]

download_pattern = [
    path('', views.select_to_download_page, name="select-to-download-page"),
    path('with/filters', views.select_to_download_filter_result_page, name="select-to-download-filter-result"),
    path('with/file/list', views.select_to_download_file_list_page, name="select-to-download-file-list"),

]

filter_pattern = [
    path('compare/environment', views.select_to_compare_filter_environment,
         name="compare-filter-region-environments"),
    path('download/environment', views.select_to_download_filter_environment,
         name="download-filter-region-environments"),
    path('compare/folder', views.select_to_compare_filter_folder,
         name="compare-filter-environment-folders"),
    path('download/folder', views.select_to_download_filter_folder,
         name="download-filter-environment-folders"),
    path('download/module/folder', views.select_to_download_filter_module_folder,
         name="download-filter-folder-modules"),
    path('download/latest/version/folder', views.select_to_download_filter_latest_version_folder,
         name="download-filter-latest-version-folder"),
]

urlpatterns = [
    path('shared_storage/compare/', include(compare_pattern)),
    path('shared_storage/download/', include(download_pattern)),
    path('shared_storage/filter/', include(filter_pattern)),
]
