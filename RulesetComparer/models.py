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
    def create_environment(self, name, full_name):
        environment = self.create(name=name, full_name=full_name)
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

    objects = EnvironmentManager()

    def __str__(self):
        return self.name


class B2BServiceManager(models.Manager):
    def create_b2b_client(self, name, url):
        service = self.create(name=name, url=url)
        return service


class B2BService(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    url = models.URLField()

    objects = B2BServiceManager()

    def __str__(self):
        return self.id


class DataCenterManager(models.Manager):
    def create_b2b_client(self, name):
        data_center = self.create(name=name)
        return data_center


class DataCenter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    objects = DataCenterManager()

    def __str__(self):
        return self.id


class B2BClientManager(models.Manager):
    def create_b2b_client(self, client_url):
        client = self.create(client_url=client_url)
        return client


class B2BClient(models.Model):
    id = models.AutoField(primary_key=True)
    data_center = models.ForeignKey(DataCenter, related_name="data_center", on_delete=models.CASCADE)
    url = models.URLField()

    objects = B2BClientManager()

    def __str__(self):
        return self.id


class B2BServerManager(models.Manager):
    def create_country_environment_server(self, country_id, environment_id, server_id, server_url):
        server = self.create(country_id=country_id, environment_id=environment_id,
                             server_id=server_id, server_url=server_url)
        return server


class B2BServer(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, related_name='country',
                                on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, related_name='environment',
                                    on_delete=models.CASCADE)
    client = models.ForeignKey(B2BClient, related_name='client',
                               on_delete=models.CASCADE)
    objects = B2BClientManager()

    def __str__(self):
        return self.id


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


class MailContentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.id


class ReportSchedulerInfoManager(models.Manager):
    def create_task(self, base_env_id, compared_env_id, module_id,
                    country_list, mail_content_type_list, mail_list_str, interval, next_proceed_time):
        task = self.create(base_environment_id=base_env_id,
                           compare_environment_id=compared_env_id,
                           module_id=module_id,
                           mail_list=mail_list_str,
                           interval_hour=interval,
                           last_proceed_time=None,
                           next_proceed_time=next_proceed_time,
                           enable=1)

        for country in country_list:
            task.country_list.add(country)

        for mail_content_type in mail_content_type_list:
            task.mail_content_type_list.add(mail_content_type)

        return task

    def update_task(self, task_id, base_env_id, compared_env_id, country_list,
                    mail_content_type_list, mail_list_str, interval, next_proceed_time):
        task = self.get(id=task_id)
        task.base_environment_id = base_env_id
        task.compare_environment_id = compared_env_id
        task.mail_list = mail_list_str
        task.interval_hour = interval
        task.next_proceed_time = next_proceed_time
        task.enable = 1

        task.country_list.clear()
        for country_id in country_list:
            task.country_list.add(country_id)

        task.mail_content_type_list.clear()
        for mail_content_type in mail_content_type_list:
            task.mail_content_type_list.add(mail_content_type)

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


class ReportSchedulerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    base_environment = models.ForeignKey(Environment, related_name='base_environment_id',
                                         on_delete=models.CASCADE)
    compare_environment = models.ForeignKey(Environment, related_name='compare_environment_id',
                                            on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='module_id', on_delete=models.CASCADE)
    country_list = models.ManyToManyField(Country)
    mail_content_type_list = models.ManyToManyField(MailContentType)
    mail_list = models.TextField()
    interval_hour = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=128, null=True)
    enable = models.IntegerField()

    objects = ReportSchedulerInfoManager()


class RulesetSyncUpSchedulerManager(models.Manager):
    def create_task(self, source_env_id, target_env_id, module,
                    country_list, action_list_str, mail_list_str,
                    interval, next_proceed_time, backup):
        task = self.create(source_environment_id=source_env_id,
                           target_environment_id=target_env_id,
                           module=module,
                           action_list=action_list_str,
                           mail_list=mail_list_str,
                           interval_hour=interval,
                           last_proceed_time=None,
                           next_proceed_time=next_proceed_time,
                           backup=backup,
                           enable=1)

        for country in country_list:
            task.country_list.add(country)

        return task

    def update_task(self, task_id, source_env_id, target_env_id,
                    country_list, action_list_str, mail_list_str,
                    interval, next_proceed_time, backup):
        task = self.get(id=task_id)
        task.source_environment_id = source_env_id
        task.target_environment_id = target_env_id
        task.action_list = action_list_str
        task.mail_list = mail_list_str
        task.interval_hour = interval
        task.next_proceed_time = next_proceed_time
        task.backup = backup

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


class RulesetSyncUpScheduler(models.Model):
    id = models.AutoField(primary_key=True)
    source_environment = models.ForeignKey(Environment, related_name='source_environment_id', on_delete=models.CASCADE)
    target_environment = models.ForeignKey(Environment, related_name='target_environment_id', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    country_list = models.ManyToManyField(Country)
    action_list = models.TextField()
    mail_list = models.TextField()
    interval_hour = models.IntegerField()
    last_proceed_time = models.DateTimeField(null=True)
    next_proceed_time = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=128, null=True)
    backup = models.IntegerField()
    enable = models.IntegerField(default=1)

    objects = RulesetSyncUpSchedulerManager()


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


class Meta:
    db_table = "RulesetComparer"
