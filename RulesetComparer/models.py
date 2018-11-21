from django.db import models


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
    def create_environment(self, name, full_name, client, account, password):
        environment = self.create(name=name, full_name=full_name, b2b_rule_set_client=client, account=account,password=password)
        return environment

    def environment_list(self, ids):
        environments = list()
        for data in ids:
            env = self.get(id=data["environment_id"])
            environments.append(env)
        return environments


class Environment(models.Model):
    name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128)
    b2b_rule_set_client = models.URLField()
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    objects = EnvironmentManager()

    def __str__(self):
        return self.name


class Meta:
    db_table = "RulesetComparer"
