from django.db import models
import uuid


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    secret_token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    website = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name

class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField()

    def __str__(self):
        return f"{self.account.name} - {self.url}"
