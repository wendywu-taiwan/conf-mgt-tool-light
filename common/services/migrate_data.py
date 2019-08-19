from RulesetComparer.models import ReportSchedulerInfo, RulesetLogGroup, RulesetSyncUpScheduler, RulesetLog


def clear_data():
    report_schedulers = ReportSchedulerInfo.objects.all()
    for report_scheduler in report_schedulers:
        try:
            base_environment = report_scheduler.base_environment
            compare_environment = report_scheduler.compare_environment
        except Exception:
            report_scheduler.delete()

    ruleset_log_groups = RulesetLogGroup.objects.all()
    for ruleset_log_group in ruleset_log_groups:
        try:
            source_environment = ruleset_log_group.source_environment
            target_environment = ruleset_log_group.target_environment
            country = ruleset_log_group.country
        except Exception:
            if RulesetLog.objects.filter(ruleset_log_group=ruleset_log_group).exists():
                RulesetLog.objects.filter(ruleset_log_group=ruleset_log_group).delete()
            ruleset_log_group.delete()

    ruleset_sync_schedulers = RulesetSyncUpScheduler.objects.all()
    for scheduler in ruleset_sync_schedulers:
        try:
            source_environment = scheduler.source_environment
            target_environment = scheduler.target_environment
        except Exception:
            scheduler.delete()
