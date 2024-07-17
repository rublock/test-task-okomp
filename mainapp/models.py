from django.db import models


class Session(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SessionUrl(models.Model):
    url = models.CharField(max_length=40)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
