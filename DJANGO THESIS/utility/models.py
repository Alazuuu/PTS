from django.db import models

# Create your models here.


class Tariff(models.Model):
    tariff_per_M = models.IntegerField()

    def __str__(self):
        return f'{self.tariff_per_M}'
