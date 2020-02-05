from django.urls import path

from RulesetComparer import views
from django.conf.urls import url, include

app_name = 'RulesetComparer'

ruleset_b2b_pattern = [
    path('create/', views.create_ruleset, name="b2b-create-ruleset"),
    path('update/', views.update_ruleset, name="b2b-update-ruleset"),
    path('scheduler/sync/all', views.get_rulesets_sync_jobs, name="get-rulesets-sync-job"),
    path('scheduler/sync/run', views.run_rulesets_sync_job, name="run-rulesets-sync-job"),
    path('scheduler/sync/create', views.create_rulesets_sync_job, name="create-rulesets-sync-job"),
    path('scheduler/sync/update', views.update_rulesets_sync_job, name="update-rulesets-sync-job"),
    path('scheduler/sync/update_status', views.update_rulesets_sync_job_status, name="update-rulesets-sync-job-status"),
    path('scheduler/sync/delete', views.delete_rulesets_sync_job, name="delete-rulesets-sync-job")
]

ruleset_pattern = [
    path('detail_download/<str:environment_id>/<str:country_id>/<str:ruleset_name>',
         views.ruleset_detail_page, name="rule-detail-download"),
    path('detail/<str:environment_id>/<str:country_id>/<str:ruleset_name>/<str:compare_key>',
         views.ruleset_detail_page, name="rule-detail"),
    path('detail_backup/<str:backup_key>/<str:backup_folder>/<str:ruleset_name>',
         views.ruleset_detail_backup_page, name="rule-detail-backup"),
    path('diff/<str:compare_key>/<str:ruleset_name>',
         views.ruleset_diff_page, name="ruleset-diff-compare-result"),
    path('diff/backup/<str:backup_key>/<str:ruleset_name>', views.ruleset_diff_backup_page, name="ruleset-diff-backup"),
    path('diff/backup/with/server/<str:backup_key>/<str:backup_folder>/<str:ruleset_name>',
         views.ruleset_diff_backup_with_server_page, name="ruleset-diff-backup-with-server"),
    path('apply/to/server',
         views.apply_ruleset_to_server, name="ruleset-apply-to-server"),
]

ruleset_download_pattern = [
    path('', views.rule_download_page, name="ruleset-download-page"),
    path('filter/', views.rule_download_filter_page, name="ruleset-download-filter-page"),
    path('packed/', views.download_rulesets, name="packed-ruleset-download"),

]
ruleset_comparer_pattern = [
    path('select/', views.environment_select_page, name="environment-select"),
    path('diff/<str:compare_key>/<str:rule_name>',
         views.ruleset_diff_page, name="rule-diff"),
    path('report/mail/<str:compare_key>',
         views.send_mail, name="report-send"),
    path('report/download/<str:compare_key>',
         views.download_compare_report, name="report-download")
]

admin_console_ruleset_pattern = [
    path('', views.admin_console_page, name="ruleset-admin-console-index"),
    path('git/country_path/list', views.admin_console_git_country_path_list_page, name="git-country-path-list"),
    path('git/country_path/edit', views.admin_console_git_country_path_edit, name="git-country-path-edit"),
    path('server_log', views.admin_console_server_log_page, name="server-log"),
    path('server_log/<int:log_type>', views.admin_console_server_log_page, name="server-log-type"),
    path('scheduler/list', views.admin_console_report_scheduler_list_page, name="report-scheduler-list"),
    path('scheduler/create', views.admin_console_report_scheduler_create_page, name="task-create"),
    path('scheduler/update/<int:scheduler_id>', views.admin_console_report_scheduler_update_page, name="task-update"),
    path('scheduler/sync/list', views.admin_console_sync_scheduler_list_page, name="sync-scheduler-list"),
    path('scheduler/sync/create', views.admin_console_sync_scheduler_create_page, name="sync-scheduler-create"),
    path('scheduler/sync/update/<int:scheduler_id>', views.admin_console_sync_scheduler_update_page,
         name="sync-scheduler-update"),
    path('recover/filter', views.admin_console_recover_ruleset_filtered_page, name="recover-filter-page"),
    path('recover/filter/environment', views.admin_console_recover_ruleset_filtered_environment_page,
         name="recover-filter-environment-page"),
    path('recover/filter/backup/list', views.admin_console_recover_ruleset_backup_list_page,
         name="recover-filter-backup-list-page"),
    path('recover/rulesets', views.recover_rulesets,
         name="recover-rulesets"),
    path('ruleset_log/list', views.admin_console_ruleset_log_list_page, name="ruleset-log-list"),
    path('ruleset_log/list/filter', views.admin_console_ruleset_log_list_filter_page, name="ruleset-log-list-filter"),
    path('ruleset_log/list/page', views.admin_console_ruleset_log_list_page_change, name="ruleset-log-list-page"),
    path('ruleset_log/detail/<int:log_id>', views.admin_console_ruleset_log_detail_page, name="ruleset-log-detail"),
    path('ruleset_log/detail/ruleset', views.get_ruleset, name="ruleset-log-detail-ruleset"),

]

admin_console_pattern = [
    path('admin_console/module/list', views.get_module_list),
    path('admin_console/module/create', views.create_module),
]

ruleset_scheduler_pattern = [
    path('<int:scheduler_id>', views.get_rulesets_report_job),
    path('list', views.get_rulesets_report_jobs),
    path('run', views.run_ruleset_report_job, name="run-report-scheduler"),
    path('create', views.create_ruleset_report_job, name="create-scheduler"),
    path('update', views.update_ruleset_report_job, name="update-scheduler"),
    path('delete', views.delete_ruleset_report_job, name="delete-scheduler"),
    path('update_status', views.update_rulesets_report_status, name="update-rulesets-report-job-status"),

]

ruleset_test_pattern = [
    path('compare/local', views.compare_ruleset_test),
]

urlpatterns = [
    path('ruleset/test/', include(ruleset_test_pattern)),
    path('ruleset/', include(ruleset_pattern)),
    path('ruleset/b2b/', include(ruleset_b2b_pattern)),
    path('ruleset/download/', include(ruleset_download_pattern)),
    path('ruleset/compare/', include(ruleset_comparer_pattern)),
    path('ruleset/scheduler/', include(ruleset_scheduler_pattern)),
    path('admin_console/ruleset/', include(admin_console_ruleset_pattern)),
]
