from django.db import models
from RulesetComparer.utils.customField import LongURLField


# Create your models here.

class CountryManager(models.Manager):
    def create_country(self, name, full_name):
        country = self.create(name=name, full_name=full_name)
        return country

    def country_list(self, ids):
        countries = list()
        for data in ids:
            country = self.get(id=data["country_id"])
            countries.append(country)
        return countries


class Country(models.Model):
    name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128, default=None)

    objects = CountryManager()

    def __str__(self):
        return self.name


class EnvironmentManager(models.Manager):
    def create_environment(self, name):
        environment = self.create(name=name)
        return environment

    def environment_list(self, ids):
        environments = list()
        for data in ids:
            env = self.get(id=data["environment_id"])
            environments.append(env)
        return environments


class Environment(models.Model):
    name = models.CharField(max_length=128)

    objects = EnvironmentManager()

    def __str__(self):
        return self.name


class B2BRuleSetServerManager(models.Manager):
    def create_server(self, country_id, env_id, user_id,password,
                      url, accessible):

        server = self.create(country_id=country_id,
                             environment_id=env_id,
                             user_id=user_id,
                             password=password,
                             url=url,
                             accessible=accessible
                             )
        return server

    def get_accessible_country_ids(self):
        return self.filter(accessible=True).values('country_id').distinct()

    def get_accessible_environment_ids(self):
        return self.filter(accessible=True).values('environment_id').distinct()



class B2BRuleSetServer(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    url = LongURLField(default="")
    accessible = models.BooleanField(default=False)

    objects = B2BRuleSetServerManager()

class RuleSetsListItem(models.Model):
    source = models.ForeignKey(B2BRuleSetServer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    pass


class RuleSetsFile(models.Model):
    pass


class RuleSet(models.Model):
    ruleSetName = models.CharField(max_length=128)
    process = models.TextField()
    organizationId = models.TextField()
    ownerRole = models.TextField()
    processStep = models.TextField()
    ruleType = models.TextField()
    key = models.TextField()
    value = models.TextField()
    expression = models.TextField()
    lastUpdatedTime = models.DateTimeField(auto_now=True)
    lastUpdatedUser = models.TextField()
    status = models.IntegerField()


class Meta:
    db_table = "RulesetComparer"
