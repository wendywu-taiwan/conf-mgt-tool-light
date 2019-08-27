from django.db import models
from django.contrib import admin


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
