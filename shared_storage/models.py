from django.db import models
from django.db.models import Q
from django.contrib import admin

from common.models import FrequencyType
from permission.models import FTPRegion, Environment, Module
from permission.utils.permission_manager import enable_environments, enable_countries
from RulesetComparer.properties.key import KEY_M_SHARED_STORAGE, KEY_F_REPORT_TASK


class SharedStorageReportSchedulerManager(models.Manager):
    def create_task(self, left_data_center_id, right_data_center_id, left_environment_id, right_environment_id,
                    left_folder, right_folder, mail_list_str, frequency_type, interval, next_proceed_time):
        task = self.create(left_data_center_id=left_data_center_id,
                           right_data_center_id=right_data_center_id,
                           left_environment_id=left_environment_id,
                           right_environment_id=right_environment_id,
                           left_folder=left_folder,
                           right_folder=right_folder,
                           mail_list=mail_list_str,
                           frequency_type=frequency_type,
                           interval=interval,
                           last_proceed_time=None,
                           next_proceed_time=next_proceed_time,
                           enable=1)
        return task

    def update_task(self, task_id, left_data_center_id, right_data_center_id, left_environment_id, right_environment_id,
                    left_folder, right_folder, mail_list_str, frequency_type, interval, next_proceed_time):
        task = self.get(id=task_id)
        task.left_data_center_id = left_data_center_id
        task.right_data_center_id = right_data_center_id
        task.left_environment_id = left_environment_id
        task.right_environment_id = right_environment_id
        task.left_folder = left_folder
        task.right_folder = right_folder
        task.mail_list = mail_list_str
        task.frequency_type = frequency_type
        task.interval = interval
        task.next_proceed_time = next_proceed_time

        task.save()
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

    def get_visible_schedulers(self, user_id):
        enable_environment_ids = enable_environments(user_id, KEY_F_REPORT_TASK, KEY_M_SHARED_STORAGE)
        query = Q()
        sub_query = Q()
        sub_query.add(Q(left_environment__in=enable_environment_ids), Q.AND)
        sub_query.add(Q(right_environment__in=enable_environment_ids), Q.AND)
        query.add(sub_query, Q.AND)

        scheduler_ids = self.filter(query).values_list("id", flat=True).distinct().order_by("id")
        array = []
        for id in scheduler_ids:
            scheduler = self.get(id=id)
            array.append(scheduler)
        return array


class SharedStorageReportScheduler(models.Model):
    id = models.AutoField(primary_key=True)
    left_data_center = models.ForeignKey(FTPRegion, related_name='s_report_scheduler_left_data_center_id',
                                         on_delete=models.PROTECT)
    right_data_center = models.ForeignKey(FTPRegion, related_name='s_report_scheduler_right_data_center_id',
                                          on_delete=models.PROTECT)
    left_environment = models.ForeignKey(Environment, related_name='s_report_scheduler_left_environment_id',
                                         on_delete=models.PROTECT)
    right_environment = models.ForeignKey(Environment, related_name='s_report_scheduler_right_environment_id',
                                          on_delete=models.PROTECT)
    left_folder = models.TextField()
    right_folder = models.TextField()
    mail_list = models.TextField()
    frequency_type = models.ForeignKey(FrequencyType, related_name='s_report_scheduler_frequency_type',
                                       on_delete=models.PROTECT, null=True)
    interval = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=128, null=True)
    enable = models.IntegerField()

    objects = SharedStorageReportSchedulerManager()


class SharedStorageReportSchedulerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'left_data_center', 'right_data_center', 'left_environment', 'right_environment', 'left_folder',
        'right_folder', 'mail_list', 'frequency_type', 'interval', 'last_proceed_time', 'next_proceed_time', 'job_id',
        'enable')


admin.site.register(SharedStorageReportScheduler, SharedStorageReportSchedulerAdmin)
