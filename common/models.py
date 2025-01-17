from django.db import models
from django.contrib import admin
from permission.models import Module, Country


# Create your models here.
class DataUpdateTimeManager(models.Manager):
    def get_data_update_time(self, table_name):
        try:
            update_time = self.get(table=table_name)
            return update_time
        except DataUpdateTime.DoesNotExist:
            return None


class DataUpdateTime(models.Model):
    id = models.AutoField(primary_key=True)
    table = models.CharField(max_length=128)
    update_time = models.DateTimeField(null=True)
    objects = DataUpdateTimeManager()


class DataUpdateTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'update_time')


admin.site.register(DataUpdateTime, DataUpdateTimeAdmin)


class FrequencyType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    interval_type = models.CharField(max_length=128)
    interval = models.IntegerField()


class FrequencyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'interval_type', 'interval')


admin.site.register(FrequencyType, FrequencyTypeAdmin)


class GitCountryPath(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, related_name='module_git_path', on_delete=models.PROTECT)
    country = models.ForeignKey(Country, related_name='country_git_path', on_delete=models.PROTECT)
    repo_path = models.CharField(max_length=128, null=True)
    folder = models.CharField(max_length=128, null=True)


class GitCountryPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'country', 'repo_path', 'folder')


admin.site.register(GitCountryPath, GitCountryPathAdmin)
