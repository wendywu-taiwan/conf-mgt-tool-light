from django.db import models
from django.contrib.auth.models import User


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
    def create_environment(self, name, full_name, active):
        environment = self.create(name=name, full_name=full_name, active=active)
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
    active = models.IntegerField(default=0)

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
    data_center = models.ForeignKey(DataCenter, related_name="data_center", on_delete=models.PROTECT)
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
                                on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, related_name='environment',
                                    on_delete=models.PROTECT)
    client = models.ForeignKey(B2BClient, related_name='client',
                               on_delete=models.PROTECT)
    objects = B2BClientManager()

    def __str__(self):
        return self.id


class ModuleManager(models.Manager):
    def create_module(self, name, display_name):
        module = self.create(name=name, display_name=display_name)
        return module


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, default=name)

    objects = ModuleManager()


class FunctionManager(models.Manager):
    def create_function(self, name, icon_file_name):
        return self.create(name=name, icon_file_name=icon_file_name)

    def get_function(self, module_name, function_name):
        module = Module.objects.get(name=module_name)
        return self.get(module=module, name=function_name)


class Function(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=128)
    icon_file_name = models.CharField(max_length=128)
    module = models.ForeignKey(Module, related_name='function_module', null=True, on_delete=models.PROTECT)

    objects = FunctionManager()


class RoleTypeManager(models.Manager):
    pass


class RoleType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)

    objects = RoleTypeManager()


class RolePermissionManager(models.Manager):
    def get_role_permission(self, role_type_name, environment_name, country_name):
        environment = Environment.objects.get(name=environment_name)
        country = Country.objects.get(name=country_name)
        role_type = RoleType.objects.get(name=role_type_name)
        return self.get(role_type=role_type, environment=environment, country=country)

    def get_role_permission_by_user_env_country_id(self, user_id, environment_id, country_id):
        role_permission_ids = self.filter(user_role_permission_role_permission__user_id=user_id,
                                          environment_id=environment_id,
                                          country_id=country_id).values_list("id", flat=True)
        if len(role_permission_ids) > 0:
            return role_permission_ids[0]
        else:
            return None


class RolePermission(models.Model):
    id = models.AutoField(primary_key=True)
    role_type = models.ForeignKey(RoleType, related_name='role_permission_role_type', on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, related_name='role_permission_env', on_delete=models.PROTECT)
    country = models.ForeignKey(Country, related_name='role_permission_country', on_delete=models.PROTECT)

    objects = RolePermissionManager()


class UserRolePermissionManager(models.Manager):
    def get_role_permission_ids(self, user):
        array = []
        if not self.filter(user=user).exists():
            return array

        permission_ids = self.filter(user=user).values_list("role_permission", flat=True)
        for permission_id in permission_ids:
            array.append(permission_id)
        return array

    def get_distinct_users(self):
        array = []
        users = self.filter().values_list("user_id", flat=True).order_by("user_id")
        for user in users:
            array.append(user)
        return array


class UserRolePermission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_role_permission_user', null=True,
                             on_delete=models.PROTECT)
    role_permission = models.ForeignKey(RolePermission, related_name='user_role_permission_role_permission',
                                        null=True, on_delete=models.PROTECT)


class RoleFunctionPermissionManager(models.Manager):
    def get_role_function_permission(self, role_permission_id, function_id):
        role_function_permission = self.filter(role_permission_id=role_permission_id, function_id=function_id).values()
        if len(role_function_permission) > 0:
            return role_function_permission[0]
        else:
            return None


class RoleFunctionPermission(models.Model):
    id = models.AutoField(primary_key=True)
    role_permission = models.ForeignKey(RolePermission, related_name='role_function_role_permission', null=True,
                                        on_delete=models.PROTECT)
    function = models.ForeignKey(Function, related_name='role_function_permission_function', null=True,
                                 on_delete=models.PROTECT)
    visible = models.IntegerField(default=0)
    editable = models.IntegerField(default=0)

    objects = RoleFunctionPermissionManager()
