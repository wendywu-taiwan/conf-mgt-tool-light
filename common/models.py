from django.db import models


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

    def __str__(self):
        return self.id


class FrequencyType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    interval_type = models.CharField(max_length=128)
    interval = models.IntegerField()

    def __str__(self):
        return self.id
