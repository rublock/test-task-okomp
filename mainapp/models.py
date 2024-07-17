from django.db import models


class Session(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Temperature(models.Model):
    time = models.CharField(max_length=255)
    temperature = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
