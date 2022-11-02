from django.db import models

# Create your models here.

class user_location(models.Model):
    locationId = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=15, null=True)
    latitude = models.CharField(max_length=15, null=True)
    longitude = models.CharField(max_length=15, null=True)

    def __str__(self):
        return str(self.userId)

