from django.db import models


# Create your models here.
class Environment(models.Model):
    userId = models.TextField()
    password = models.TextField()
    country = models.TextField(default='Taiwan')
    environment = models.TextField(default='Int1')
    url = models.TextField()


class RuleSet(models.Model):
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
