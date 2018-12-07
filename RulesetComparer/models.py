from django.db import models


# Create your models here.

class CountryManager(models.Manager):
    def create_country(self, name, full_name, icon_file_name):
        country = self.create(name=name, full_name=full_name, icon_file_name=icon_file_name)
        return country

    def country_list(self, ids):
        countries = list()
        for data in ids:
            country = self.get(id=data["country_id"])
            countries.append(country)
        return countries


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128, default=None, blank=True, null=True)
    icon_file_name = models.CharField(max_length=128, default=None, blank=True, null=True)

    objects = CountryManager()

    def __str__(self):
        return self.name


class EnvironmentManager(models.Manager):
    def create_environment(self, name, full_name, client):
        environment = self.create(name=name, full_name=full_name, b2b_rule_set_client=client)
        return environment

    def environment_list(self, ids):
        environments = list()
        for data in ids:
            env = self.get(id=data["environment_id"])
            environments.append(env)
        return environments


class Environment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128)
    b2b_rule_set_client = models.URLField()

    objects = EnvironmentManager()

    def __str__(self):
        return self.name


class FunctionManager(models.Manager):
    def create_function(self, name, icon_file_name):
        function = self.create(name=name, icon_file_name=icon_file_name)
        return function


class Function(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=128)
    icon_file_name = models.CharField(max_length=128)
    objects = FunctionManager()


class ModuleManager(models.Manager):
    def create_module(self, name, icon_file_name):
        module = self.create(name=name, icon_file_name=icon_file_name)
        return module


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    icon_file_name = models.CharField(max_length=128, default=None, blank=True, null=True)
    functions = models.ManyToManyField(Function)

    objects = ModuleManager()


class UserRoleManager(models.Manager):
    def create_user_role(self, name, modules):
        user_role = self.create(name=name, modules=modules)
        return user_role


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    modules = models.ManyToManyField(Module)

    objects = UserRoleManager()


class ReportSchedulerInfoManager(models.Manager):
    def create_task(self, base_env_id, compared_env_id, module_id,
                    country_list, mail_list_str, interval, next_proceed_time):
        test_task = self.create(base_environment_id=base_env_id,
                                compare_environment_id=compared_env_id,
                                module_id=module_id,
                                mail_list=mail_list_str,
                                interval_hour=interval,
                                last_proceed_time=None,
                                next_proceed_time=next_proceed_time,
                                enable=1)

        for country in country_list:
            test_task.country_list.add(country)

        return test_task


class ReportSchedulerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    base_environment = models.ForeignKey(Environment, related_name='base_environment_id',
                                         on_delete=models.CASCADE)
    compare_environment = models.ForeignKey(Environment, related_name='compare_environment_id',
                                            on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='module_id', on_delete=models.CASCADE)
    country_list = models.ManyToManyField(Country)
    mail_list = models.TextField()
    interval_hour = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    enable = models.IntegerField()

    objects = ReportSchedulerInfoManager()


class TestScheduledTaskManager(models.Manager):
    def create_task(self, status):
        test_task = self.create(status=status)
        return test_task


class TestScheduledTask(models.Model):
    status = models.IntegerField()

    objects = TestScheduledTaskManager()


class Meta:
    db_table = "RulesetComparer"
