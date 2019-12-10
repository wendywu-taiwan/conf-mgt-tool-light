import traceback
from shutil import copyfile

from django.template.loader import render_to_string

from RulesetComparer.date_model.json_builder.compare_report_info import CompareReportInfoBuilder
from RulesetComparer.task.compare_ruleset_list import CompareRuleListTask
from RulesetComparer.task.ruleset_daily_report import RulesetDailyReportTask, timeUtil
from RulesetComparer.date_model.json_parser.create_report_scheduler import CreateReportSchedulerParser
from RulesetComparer.date_model.json_parser.db_report_scheduler import DBReportSchedulerParser
from RulesetComparer.date_model.json_parser.delete_report_scheduler import DeleteReportSchedulerParser
from RulesetComparer.date_model.json_parser.update_report_scheduler_status import UpdateReportSchedulerStatusParser
from RulesetComparer.models import ReportSchedulerInfo
from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.utils.logger import info_log, error_log
from RulesetComparer.properties.key import *
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.mailSender import MailSender
from common.properties.config import RULESET_COMPARE_RESULT_FOLDER_PATH, RULESET_COMPARE_RESULT_HTML, \
    RULESET_COMPARE_RESULT_ZIP_RESOURCE, RULESET_ZIP_FILE_PATH, RULESET_ZIP_PATH
from common.properties.time_setting import YEAR_MONTH_DATE
from common.properties.mail_setting import SEND_RULESET_COMPARE_RESULT_MAIL
from permission.models import Environment
from permission.data_object.permission_checker import RulesetReportPermissionChecker


def restart_schedulers():
    try:
        schedulers = ReportSchedulerInfo.objects.all()
        if len(schedulers) == 0:
            return

        info_log("rulesetReportSchedulerService", "restart all schedulers")
        for scheduler in schedulers:
            country_list = scheduler.country_list.values(KEY_ID)
            mail_content_type_list = scheduler.mail_content_type_list.values(KEY_ID)
            parser = DBReportSchedulerParser(scheduler, country_list, mail_content_type_list)
            ReportSchedulerInfo.objects.update_next_proceed_time(parser.task_id, parser.utc_time)
            add_task_to_scheduler(parser)
        info_log("rulesetReportSchedulerService", "restart all success")

    except Exception as e:
        raise e


def get_schedulers():
    try:
        schedulers = ReportSchedulerInfo.objects.all()
        return schedulers
    except Exception as e:
        raise e


def run_scheduler_now(json_data, user):
    try:
        scheduler = ReportSchedulerInfo.objects.get(id=json_data.get(KEY_ID))
        country_id_list = scheduler.country_list.values(KEY_ID)
        mail_content_type_list = scheduler.mail_content_type_list.values(KEY_ID)

        parser = DBReportSchedulerParser(scheduler, country_id_list, mail_content_type_list)
        base_env = Environment.objects.get(id=parser.base_env_id)
        compare_env = Environment.objects.get(id=parser.compare_env_id)
        RulesetReportPermissionChecker(user, parser.country_list, base_env.id, compare_env.id)

        for country in parser.country_list:
            task = CompareRuleListTask(base_env.id, compare_env.id, country.id)

            # generate mail content
            result_data = fileManager.load_compare_result_file(task.compare_hash_key)
            info_builder = CompareReportInfoBuilder(result_data, parser.mail_content_type_list)
            content_json = info_builder.get_data()
            html_content = render_to_string('compare_info_mail_content.html', content_json)

            if content_json[COMPARE_RESULT_HAS_CHANGES]:
                zip_file_path = generate_report_mail_attachment(task)
                send_report_mail_with_attachment(country.name, base_env.name, compare_env.name, html_content,
                                                 parser.mail_list, zip_file_path)
            else:
                send_report_mail(country.name, base_env.name, compare_env.name, html_content, parser.mail_list)
    except Exception as e:
        error_log(e)
        error_log(traceback.format_exc())


def create_scheduler(json_data, user):
    parser = CreateReportSchedulerParser(json_data, user)
    RulesetReportPermissionChecker(user, parser.country_list, parser.base_env_id, parser.compare_env_id)
    report_scheduler = ReportSchedulerInfo.objects.create_task(parser.base_env_id,
                                                               parser.compare_env_id,
                                                               parser.module_id,
                                                               parser.country_list,
                                                               parser.mail_content_type_list,
                                                               parser.mail_list,
                                                               parser.frequency_type,
                                                               parser.interval,
                                                               parser.utc_time)

    parser.task_id = report_scheduler.id
    add_task_to_scheduler(parser)
    return report_scheduler


def update_report_scheduler(json_data, user):
    try:
        parser = CreateReportSchedulerParser(json_data, user)
        RulesetReportPermissionChecker(user, parser.country_list, parser.base_env_id, parser.compare_env_id)
        report_scheduler = ReportSchedulerInfo.objects.update_task(parser.task_id,
                                                                   parser.base_env_id,
                                                                   parser.compare_env_id,
                                                                   parser.country_list,
                                                                   parser.mail_content_type_list,
                                                                   parser.mail_list,
                                                                   parser.frequency_type,
                                                                   parser.interval,
                                                                   parser.utc_time)
        add_task_to_scheduler(parser)
        return report_scheduler
    except Exception as e:
        raise e


def delete_scheduler(json_data, user):
    parser = DeleteReportSchedulerParser(json_data, user)
    RulesetReportPermissionChecker(user, parser.country_id_list, parser.base_env_id, parser.compare_env_id)
    ReportSchedulerInfo.objects.filter(id=parser.task_id).delete()


def add_task_to_scheduler(parser):
    task = RulesetDailyReportTask(parser)
    scheduler = CustomJobScheduler()
    if parser.frequency_type.interval_type == KEY_DAYS:
        job = scheduler.add_days_job(task.run_task, parser.interval, parser.local_time)
    elif parser.frequency_type.interval_type == KEY_WEEKS:
        job = scheduler.add_weeks_job(task.run_task, parser.interval, parser.local_time)
    else:
        job = scheduler.add_months_job(task.run_task, parser.interval, parser.local_time)

    ReportSchedulerInfo.objects.update_job_id(parser.task_id, job.id)
    task.set_scheduled_job(job)


def update_scheduler_status(json_data, user):
    parser = UpdateReportSchedulerStatusParser(json_data, user)
    task = ReportSchedulerInfo.objects.update_task_status(parser.task_id, parser.enable)
    return task


def generate_report_mail_attachment(task):
    copy_path = RULESET_COMPARE_RESULT_FOLDER_PATH % str(task.compare_hash_key)
    fileManager.create_folder(copy_path)

    resource_full_path = RULESET_COMPARE_RESULT_HTML % task.compare_hash_key
    copy_full_path = RULESET_COMPARE_RESULT_ZIP_RESOURCE % (
        task.compare_hash_key, task.compare_hash_key)
    copyfile(resource_full_path, copy_full_path)

    # archive single folder report
    zip_file_path = RULESET_ZIP_FILE_PATH % task.compare_hash_key
    fileManager.archive_file_with_arcname(copy_path, RULESET_ZIP_PATH, zip_file_path)
    fileManager.clear_folder(copy_path)
    return zip_file_path


def send_report_mail(country_name, base_env_name, compare_env_name, mail_content, receivers):
    send_report_mail_with_attachment(country_name, base_env_name, compare_env_name, mail_content, receivers, None)


def send_report_mail_with_attachment(country_name, base_env_name, compare_env_name, mail_content, receivers,
                                     attachment_path=None):
    current_time = timeUtil.get_format_current_time(YEAR_MONTH_DATE)

    subject = SEND_RULESET_COMPARE_RESULT_MAIL.get("title")
    subject = subject + " for " + country_name + " - " + base_env_name + " <> " + compare_env_name

    mail_sender = MailSender(SEND_RULESET_COMPARE_RESULT_MAIL)

    if attachment_path:
        file_name = current_time + "_" + base_env_name + "_" + compare_env_name + "_" + country_name + "_" + "compare_report.zip"
        mail_sender.add_attachment(attachment_path, file_name, "text")

    mail_sender.set_receiver(receivers)
    mail_sender.compose_msg(subject, None, mail_content)
    mail_sender.send()
    mail_sender.quit()
    info_log("ruleset report service", "send report mail success")
