from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)