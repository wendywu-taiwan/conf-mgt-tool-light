import traceback

from RulesetComparer.task.clear_report_files import ClearCompareReportFilesTask
from RulesetComparer.task.clear_ruleset_files import ClearRulesetFilesTask
from RulesetComparer.task.clear_ruleset_zip_files import ClearRulesetArchivedFilesTask
from shared_storage.task.clear_tmp_files import ClearTmpFilesTask
from shared_storage.task.clear_compare_result_files import ClearCompareResultTask
from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.utils.logger import info_log, error_log
from RulesetComparer.services import report_scheduler, sync_scheduler


def restart_all_scheduler():
    try:
        # clear zip and ruleset file scheduler
        clear_zip_ruleset_task = ClearRulesetArchivedFilesTask()
        clear_ruleset_task = ClearRulesetFilesTask()
        clear_compare_report_task = ClearCompareReportFilesTask()
        clear_ss_tmp_file_task = ClearTmpFilesTask()
        clear_ss_compare_result_task = ClearCompareResultTask()
        info_log(None, "restart clear scheduler")
        scheduler = CustomJobScheduler()
        scheduler.add_hours_job_now(clear_ruleset_task.run_task, 24)
        scheduler.add_hours_job_now(clear_zip_ruleset_task.run_task, 24)
        scheduler.add_hours_job_now(clear_compare_report_task.run_task, 24)
        scheduler.add_hours_job_now(clear_ss_tmp_file_task.run_task, 24)
        scheduler.add_hours_job_now(clear_ss_compare_result_task.run_task, 24)
        info_log(None, "restart clear scheduler success")
        report_scheduler.restart_schedulers()
        sync_scheduler.restart_schedulers()
    except BaseException as e:
        error_log(traceback.format_exc())
        raise e
