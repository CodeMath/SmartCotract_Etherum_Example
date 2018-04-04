from django.db import models
from django.contrib.auth.models import User

class transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    funding = models.CharField(max_length=255, default="Test")
    txid = models.CharField(max_length=255)

    def __str__(self):
        return "%s" %(txid)
