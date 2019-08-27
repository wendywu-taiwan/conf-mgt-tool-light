from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


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


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'full_name', 'icon_file_name')


admin.site.register(Country, CountryAdmin)


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


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'full_name', 'active')


admin.site.register(Environment, EnvironmentAdmin)


class B2BServiceManager(models.Manager):
    def create_b2b_client(self, name, url):
        service = self.create(name=name, url=url)
        return service


class B2BService(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    url = models.URLField()

    objects = B2BServiceManager()


class B2BServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')


admin.site.register(B2BService, B2BServiceAdmin)


class DataCenterManager(models.Manager):
    def create_b2b_client(self, name):
        data_center = self.create(name=name)
        return data_center


class DataCenter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    objects = DataCenterManager()


class DataCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(DataCenter, DataCenterAdmin)


class B2BClientManager(models.Manager):
    def create_b2b_client(self, client_url):
        client = self.create(client_url=client_url)
        return client


class B2BClient(models.Model):
    id = models.AutoField(primary_key=True)
    data_center = models.ForeignKey(DataCenter, related_name="data_center", on_delete=models.PROTECT)
    url = models.URLField()

    objects = B2BClientManager()


class B2BClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_center', 'url')


admin.site.register(B2BClient, B2BClientAdmin)


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


class B2BServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'environment', 'client')


admin.site.register(B2BServer, B2BServerAdmin)


class ModuleManager(models.Manager):
    def create_module(self, name, display_name):
        module = self.create(name=name, display_name=display_name)
        return module


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, default=name)

    objects = ModuleManager()


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name')


admin.site.register(Module, ModuleAdmin)


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


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon_file_name', 'module')


admin.site.register(Function, FunctionAdmin)


class RoleTypeManager(models.Manager):
    pass


class RoleType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)

    objects = RoleTypeManager()


class RoleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name')


admin.site.register(RoleType, RoleTypeAdmin)


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

    def filter_by_environment_role_type(self, environment_id, role_type_id):
        return self.filter(environment_id=environment_id, role_type_id=role_type_id).values_list("id", flat=True)


class RolePermission(models.Model):
    id = models.AutoField(primary_key=True)
    role_type = models.ForeignKey(RoleType, related_name='role_permission_role_type', on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, related_name='role_permission_env', on_delete=models.PROTECT)
    country = models.ForeignKey(Country, related_name='role_permission_country', on_delete=models.PROTECT)

    objects = RolePermissionManager()


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_type', 'environment', 'country')


admin.site.register(RolePermission, RolePermissionAdmin)


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


class UserRolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role_permission')


admin.site.register(UserRolePermission, UserRolePermissionAdmin)


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


class RoleFunctionPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_permission', 'function', 'visible', 'editable')


admin.site.register(RoleFunctionPermission, RoleFunctionPermissionAdmin)


class FTPClient(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    data_center = models.CharField(max_length=128)
    port = models.IntegerField(default=0)


class FTPServer(models.Model):
    id = models.AutoField(primary_key=True)
    ftp_client = models.ForeignKey(FTPClient, related_name='ftp_server_key_client', null=True,
                                   on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, related_name='ftp_server_key_environment', null=True,
                                    on_delete=models.PROTECT)
