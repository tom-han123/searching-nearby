from django.db import models

# Create your models here.

class user_location(models.Model):
    locationId = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=15, null=True, unique=True)
    user_first_name = models.CharField(max_length=20,null=True, blank=True)
    user_last_name = models.CharField(max_length=20,null=True,blank=True)
    image = models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=20,null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    latitude = models.CharField(max_length=15, null=True)
    longitude = models.CharField(max_length=15, null=True)

    def __str__(self):
        return str(self.user_first_name)

