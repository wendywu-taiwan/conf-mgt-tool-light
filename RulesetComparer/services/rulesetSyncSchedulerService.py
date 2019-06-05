from RulesetComparer.b2bRequestTask.rulesetsSyncUpTask import RulesetsSyncUpTask
from RulesetComparer.dataModel.dataParser.createRulesetSyncSchedulerParser import CreateRulesetSyncSchedulerParser
from RulesetComparer.dataModel.dataParser.dbRulesetSyncSchedulerParser import DBRulesetSyncSchedulerParser
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
                                                                    parser.interval_hour,
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
                                                                    parser.interval_hour,
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
    job = scheduler.add_hours_job(task.run_task, parser.interval_hour, parser.local_time)
    # save job id to database
    RulesetSyncUpScheduler.objects.update_job_id(db_scheduler_id, job.id)
    task.set_scheduled_job(job)


def delete_scheduler(json_data):
    task_id = json_data.get(KEY_TASK_ID)
    RulesetSyncUpScheduler.objects.get(id=task_id).delete()


def update_scheduler_status(json_data):
    task_id = json_data.get(KEY_TASK_ID)
    enable = json_data.get(KEY_ENABLE)
    if enable:
        enable = 1
    else:
        enable = 0
    task = RulesetSyncUpScheduler.objects.update_task_status(task_id, enable)
    return task
