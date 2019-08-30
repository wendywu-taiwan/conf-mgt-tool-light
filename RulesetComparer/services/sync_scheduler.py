from RulesetComparer.task.rulesets_sync import RulesetsSyncUpTask
from RulesetComparer.date_model.json_parser.create_ruleset_sync_scheduler import CreateRulesetSyncSchedulerParser
from RulesetComparer.date_model.json_parser.update_sync_scheduler_status import UpdateSyncSchedulerStatusParser
from RulesetComparer.date_model.json_parser.db_ruleset_sync_scheduler import DBRulesetSyncSchedulerParser
from RulesetComparer.date_model.json_parser.delete_sync_scheduler import DeleteSyncSchedulerParser
from RulesetComparer.models import RulesetSyncUpScheduler

from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.utils.logger import *


def restart_schedulers():
    try:
        schedulers = RulesetSyncUpScheduler.objects.all()
        if len(schedulers) == 0:
            return

        info_log("rulesetSyncUpService", "restart all schedulers")
        for scheduler in schedulers:
            country_list = scheduler.country_list.values(KEY_ID)
            parser = DBRulesetSyncSchedulerParser(scheduler, country_list)
            RulesetSyncUpScheduler.objects.update_next_proceed_time(parser.task_id, parser.utc_time)
            add_task_to_scheduler(scheduler.id, parser)
        info_log("rulesetSyncUpService", "restart all schedulers success")

    except Exception as e:
        raise e


def get_schedulers():
    try:
        schedulers = RulesetSyncUpScheduler.objects.all()
        return schedulers
    except Exception as e:
        raise e


def create_scheduler(json_data, user):
    try:
        parser = CreateRulesetSyncSchedulerParser(json_data, user)
        sync_scheduler = RulesetSyncUpScheduler.objects.create_task(parser.source_environment_id,
                                                                    parser.target_environment_id,
                                                                    parser.module,
                                                                    parser.country_list,
                                                                    parser.action_list,
                                                                    parser.receiver_list,
                                                                    parser.frequency_type,
                                                                    parser.interval,
                                                                    parser.utc_time,
                                                                    parser.creator,
                                                                    parser.created_time)
        parser.set_task_id(sync_scheduler.id)
        add_task_to_scheduler(sync_scheduler.id, parser)
        return sync_scheduler
    except Exception as e:
        raise e


def update_scheduler(json_data, user):
    try:
        parser = CreateRulesetSyncSchedulerParser(json_data, user)
        sync_scheduler = RulesetSyncUpScheduler.objects.update_task(parser.task_id,
                                                                    parser.source_environment_id,
                                                                    parser.target_environment_id,
                                                                    parser.country_list,
                                                                    parser.action_list,
                                                                    parser.receiver_list,
                                                                    parser.frequency_type,
                                                                    parser.interval,
                                                                    parser.utc_time,
                                                                    parser.editor,
                                                                    parser.updated_time)
        add_task_to_scheduler(sync_scheduler.id, parser)
        return sync_scheduler
    except Exception as e:
        raise e


def add_task_to_scheduler(db_scheduler_id, parser):
    task = RulesetsSyncUpTask(parser)
    scheduler = CustomJobScheduler()
    if parser.frequency_type.interval_type == KEY_DAYS:
        job = scheduler.add_days_job(task.run_task, parser.interval, parser.local_time)
    elif parser.frequency_type.interval_type == KEY_WEEKS:
        job = scheduler.add_weeks_job(task.run_task, parser.interval, parser.local_time)
    else:
        job = scheduler.add_months_job(task.run_task, parser.interval, parser.local_time)
    # save job id to database
    RulesetSyncUpScheduler.objects.update_job_id(db_scheduler_id, job.id)
    task.set_scheduled_job(job)


def delete_scheduler(json_data, user):
    parser = DeleteSyncSchedulerParser(json_data, user)
    RulesetSyncUpScheduler.objects.get(id=parser.task_id).delete()


def update_scheduler_status(json_data, user):
    parser = UpdateSyncSchedulerStatusParser(json_data, user)
    task = RulesetSyncUpScheduler.objects.update_task_status(parser.task_id, parser.enable)
    return task
