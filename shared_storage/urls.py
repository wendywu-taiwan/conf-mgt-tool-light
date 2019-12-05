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
    path('files', views.download_files, name="select-to-download-files"),
    path('exist/files', views.download_exist_files, name="select-to-download-exist-files"),

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

admin_console_pattern = [
    path('', views.admin_console_page, name="admin-console-index"),
    path('report/scheduler/list', views.admin_console_report_scheduler_list_page, name="report-scheduler-list-page"),
    path('report/scheduler/create', views.admin_console_report_scheduler_create_page,
         name="report-scheduler-create-page"),
    path('report/scheduler/update/<int:scheduler_id>', views.admin_console_report_scheduler_update_page,
         name="report-scheduler-update-page"),
]

admin_console_report_api_pattern = [
    path('create', views.create_report_scheduler_job, name="create-report-scheduler"),
    path('update', views.update_report_scheduler_job, name="update-report-scheduler"),
    path('delete', views.delete_report_scheduler_job, name="delete-report-scheduler"),
    path('update_status', views.update_report_scheduler_status, name="update-report-scheduler-status"),
]

urlpatterns = [
    path('shared_storage/compare/', include(compare_pattern)),
    path('shared_storage/download/', include(download_pattern)),
    path('shared_storage/filter/', include(filter_pattern)),
    path('shared_storage/report/scheduler/', include(admin_console_report_api_pattern)),
    path('admin_console/shared_storage/', include(admin_console_pattern)),

]
