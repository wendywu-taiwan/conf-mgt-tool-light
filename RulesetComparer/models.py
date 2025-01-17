from django.db import models
from django.db.models import Q
from django.contrib import admin

from permission.models import Environment, Country, Module
from common.models import FrequencyType
from permission.utils.permission_manager import *
from django.contrib.auth.models import User


class MailContentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)


class MailContentTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'title')


admin.site.register(MailContentType, MailContentTypeAdmin)


class ReportSchedulerInfoManager(models.Manager):
    def create_task(self, base_env_id, compared_env_id, module_id,
                    country_list, mail_content_type_list, mail_list_str, frequency_type,
                    interval, next_proceed_time, display_name, skip_ruleset_list):
        task = self.create(base_environment_id=base_env_id,
                           compare_environment_id=compared_env_id,
                           module_id=module_id,
                           mail_list=mail_list_str,
                           frequency_type=frequency_type,
                           interval=interval,
                           last_proceed_time=None,
                           next_proceed_time=next_proceed_time,
                           enable=1,
                           display_name=display_name)

        for country in country_list:
            task.country_list.add(country)

        for mail_content_type in mail_content_type_list:
            task.mail_content_type_list.add(mail_content_type)

        for skip_tuple in skip_ruleset_list:
            country = skip_tuple[0]
            ruleset_list = skip_tuple[1]
            ReportSchedulerSkipRuleset.objects.create(report_scheduler=task, country=country, ruleset_list=ruleset_list)

        return task

    def update_task(self, task_id, base_env_id, compared_env_id, country_list,
                    mail_content_type_list, mail_list_str, frequency_type, interval, next_proceed_time, display_name,
                    skip_ruleset_list):
        task = self.get(id=task_id)
        task.base_environment_id = base_env_id
        task.compare_environment_id = compared_env_id
        task.mail_list = mail_list_str
        task.frequency_type = frequency_type
        task.interval = interval
        task.next_proceed_time = next_proceed_time
        task.display_name = display_name

        task.country_list.clear()
        for country_id in country_list:
            task.country_list.add(country_id)

        task.mail_content_type_list.clear()
        for mail_content_type in mail_content_type_list:
            task.mail_content_type_list.add(mail_content_type)

        task.skip_rulesets.all().delete()
        task.save()

        for skip_tuple in skip_ruleset_list:
            country = skip_tuple[0]
            ruleset_list = skip_tuple[1]
            ReportSchedulerSkipRuleset.objects.create(report_scheduler=task, country=country,
                                                      ruleset_list=ruleset_list)
        return task

    def update_next_proceed_time(self, task_id, next_proceed_time):
        task = self.get(id=task_id)
        task.next_proceed_time = next_proceed_time

        task.save()
        return task

    def update_job_id(self, task_id, job_id):
        task = self.get(id=task_id)
        task.job_id = job_id
        task.save()
        return task

    def update_task_status(self, task_id, enable):
        task = self.get(id=task_id)
        task.enable = enable
        task.save()
        return task

    def get_visible_schedulers(self, user_id, module):
        enable_environment_ids = enable_environments(user_id, KEY_F_REPORT_TASK, module)
        query = Q()
        query.add(Q(module__name=module), Q.AND)

        for environment_id in enable_environment_ids:
            sub_query = Q()
            country_ids = enable_countries(user_id, environment_id)
            sub_query.add(Q(base_environment__in=enable_environment_ids), Q.AND)
            sub_query.add(Q(compare_environment__in=enable_environment_ids), Q.AND)
            sub_query.add(Q(country_list__country__id__in=country_ids), Q.AND)
            query.add(sub_query, Q.AND)

        scheduler_ids = self.filter(query).values_list("id", flat=True).distinct().order_by("id")
        array = []
        for id in scheduler_ids:
            scheduler = self.get(id=id)
            array.append(scheduler)
        return array


class ReportSchedulerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    base_environment = models.ForeignKey(Environment, related_name='base_environment_id',
                                         on_delete=models.PROTECT)
    compare_environment = models.ForeignKey(Environment, related_name='compare_environment_id',
                                            on_delete=models.PROTECT)
    module = models.ForeignKey(Module, related_name='module_id', on_delete=models.PROTECT)
    country_list = models.ManyToManyField(Country)
    mail_content_type_list = models.ManyToManyField(MailContentType)
    mail_list = models.TextField()
    frequency_type = models.ForeignKey(FrequencyType, related_name='report_scheduler_frequency_type',
                                       on_delete=models.PROTECT, null=True)
    interval = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=128, null=True)
    enable = models.IntegerField()
    display_name = models.CharField(max_length=128, null=True)

    objects = ReportSchedulerInfoManager()


class ReportSchedulerInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'base_environment', 'compare_environment', 'module',
        'mail_list', 'frequency_type', 'interval', 'last_proceed_time', 'next_proceed_time', 'job_id', 'enable',
        'display_name')


admin.site.register(ReportSchedulerInfo, ReportSchedulerInfoAdmin)


# Create your models here.
class ReportSchedulerSkipRulesetManager(models.Manager):
    pass


class ReportSchedulerSkipRuleset(models.Model):
    id = models.AutoField(primary_key=True)
    report_scheduler = models.ForeignKey(ReportSchedulerInfo, related_name='skip_rulesets',
                                         on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    ruleset_list = models.TextField()

    objects = ReportSchedulerSkipRulesetManager()


class RulesetSyncUpSchedulerManager(models.Manager):
    def create_task(self, source_env_id, target_env_id, module,
                    country_list, action_list_str, mail_list_str,
                    frequency_type, interval, next_proceed_time, creator, created_time):
        task = self.create(source_environment_id=source_env_id,
                           target_environment_id=target_env_id,
                           module=module,
                           action_list=action_list_str,
                           mail_list=mail_list_str,
                           frequency_type=frequency_type,
                           interval=interval,
                           last_proceed_time=None,
                           next_proceed_time=next_proceed_time,
                           creator=creator,
                           created_time=created_time,
                           editor=creator,
                           updated_time=created_time,
                           enable=1)

        for country in country_list:
            task.country_list.add(country)

        return task

    def update_task(self, task_id, source_env_id, target_env_id,
                    country_list, action_list_str, mail_list_str,
                    frequency_type, interval, next_proceed_time, editor, updated_time):
        task = self.get(id=task_id)
        task.source_environment_id = source_env_id
        task.target_environment_id = target_env_id
        task.action_list = action_list_str
        task.mail_list = mail_list_str
        task.frequency_type = frequency_type
        task.interval = interval
        task.next_proceed_time = next_proceed_time
        task.editor = editor
        task.updated_time = updated_time

        task.country_list.clear()
        for country_id in country_list:
            task.country_list.add(country_id)

        task.save()
        return task

    def update_time(self, task_id, last_proceed_time, next_proceed_time):
        task = self.get(id=task_id)
        task.last_proceed_time = last_proceed_time
        task.next_proceed_time = next_proceed_time
        task.save()
        return task

    def update_next_proceed_time(self, task_id, next_proceed_time):
        task = self.get(id=task_id)
        task.next_proceed_time = next_proceed_time

        task.save()
        return task

    def update_task_status(self, task_id, enable):
        task = self.get(id=task_id)
        task.enable = enable
        task.save()
        return task

    def update_job_id(self, task_id, job_id):
        task = self.get(id=task_id)
        task.job_id = job_id
        task.save()
        return task

    def filter_environments_and_countries(self, user_id, environment_ids):
        query = Q()
        for environment_id in environment_ids:
            sub_query = Q()
            country_ids = enable_countries(user_id, environment_id)
            sub_query.add(Q(target_environment=environment_id), Q.AND)
            sub_query.add(Q(country_list__country__id__in=country_ids), Q.AND)
            query.add(sub_query, Q.OR)

        scheduler_ids = self.filter(query).values_list("id", flat=True).distinct().order_by("id")
        array = []
        for id in scheduler_ids:
            scheduler = self.get(id=id)
            array.append(scheduler)
        return array


class RulesetSyncUpScheduler(models.Model):
    id = models.AutoField(primary_key=True)
    source_environment = models.ForeignKey(Environment, related_name='source_environment_id', on_delete=models.PROTECT)
    target_environment = models.ForeignKey(Environment, related_name='target_environment_id', on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    country_list = models.ManyToManyField(Country)
    action_list = models.TextField()
    mail_list = models.TextField()
    frequency_type = models.ForeignKey(FrequencyType, related_name='sync_scheduler_frequency_type',
                                       on_delete=models.PROTECT, null=True)
    interval = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=128, null=True)
    enable = models.IntegerField(default=1)
    creator = models.ForeignKey(User, null=True, related_name='task_creator',
                                on_delete=models.PROTECT)
    editor = models.ForeignKey(User, null=True, related_name='task_editor', on_delete=models.PROTECT)
    created_time = models.DateTimeField(null=True)
    updated_time = models.DateTimeField(null=True)

    objects = RulesetSyncUpSchedulerManager()


class RulesetSyncUpSchedulerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'source_environment', 'target_environment', 'module', 'action_list', 'mail_list',
        'frequency_type', 'interval', 'last_proceed_time', 'next_proceed_time', 'job_id', 'enable', 'creator', 'editor',
        'created_time', 'updated_time')


admin.site.register(RulesetSyncUpScheduler, RulesetSyncUpSchedulerAdmin)


class RulesetLogGroup(models.Model):
    id = models.AutoField(primary_key=True)
    backup_key = models.CharField(max_length=128)
    update_time = models.DateTimeField(null=True)
    task = models.ForeignKey(RulesetSyncUpScheduler, related_name='rs_log_group_task', on_delete=models.SET_NULL,
                             null=True)
    source_environment = models.ForeignKey(Environment, related_name='rs_log_group_source_env',
                                           on_delete=models.PROTECT, null=True)
    target_environment = models.ForeignKey(Environment, related_name='rs_log_group_target_env',
                                           on_delete=models.PROTECT)
    author = models.ForeignKey(User, related_name='rs_log_group_author', null=True,
                               on_delete=models.PROTECT)
    country = models.ForeignKey(Country, related_name='rs_log_group_country', on_delete=models.PROTECT)
    commit_sha = models.CharField(max_length=128, null=True)
    created = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    deleted = models.IntegerField(default=0)
    log_count = models.IntegerField(default=0)


class RulesetLogGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'backup_key', 'update_time', 'task', 'source_environment', 'target_environment', 'author', 'country',
        'created', 'updated', 'deleted', 'log_count')


admin.site.register(RulesetLogGroup, RulesetLogGroupAdmin)


class RulesetAction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    capital_name = models.CharField(max_length=128)


class RulesetActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capital_name')


admin.site.register(RulesetAction, RulesetActionAdmin)


class RulesetLogManager(models.Manager):
    def get_ruleset_log(self, log_id):
        log = self.filter(id=log_id).values()
        return log[0]


class RulesetLog(models.Model):
    id = models.AutoField(primary_key=True)
    ruleset_log_group = models.ForeignKey(RulesetLogGroup, related_name='ruleset_log_group',
                                          on_delete=models.PROTECT)
    action = models.ForeignKey(RulesetAction, related_name='ruleset_action', on_delete=models.PROTECT)
    ruleset_name = models.CharField(max_length=128)
    status = models.IntegerField(default=1)
    exception = models.CharField(max_length=128, null=True)

    objects = RulesetLogManager()


class RulesetLogPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruleset_log_group', 'action', 'ruleset_name', 'status', 'exception')


admin.site.register(RulesetLog, RulesetLogPermissionAdmin)


class Meta:
    db_table = "RulesetComparer"
