from django.db import models


class Session(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    country_id = models.IntegerField()
    region_id = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class SessionUrl(models.Model):
    url = models.CharField(max_length=40)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
