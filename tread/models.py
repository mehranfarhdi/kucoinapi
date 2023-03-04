from django.db import models


class Coin(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    symbol = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ExitAndEnterFactor(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    profit_coefficient = models.FloatField()
    limit_coefficient = models.FloatField()

    def __str__(self):
        return str(self.name)
