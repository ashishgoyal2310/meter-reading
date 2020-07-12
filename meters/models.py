from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class UserMeter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_meters'
    )
    meter_number = models.CharField(max_length = 16, unique=True)
    address = models.TextField()
    state = models.CharField(max_length = 16)
    zipcode = models.CharField(max_length = 6)
    install_date = models.DateField(auto_now=False, auto_now_add=True)
    location = models.CharField(max_length=32)
    siteid = models.CharField(max_length=32)
    configurations = models.CharField(max_length=32, default='2TB')
    warranty = models.CharField(max_length=32)
    model_type = models.CharField(max_length=32)
    
    def __str__(self):
        return '%s %s' % (self.user, self.meter_number)


class MeterHealth(models.Model):
    user_meter = models.ForeignKey(UserMeter, on_delete=models.CASCADE,related_name='meterhealths')
    meter_status = models.CharField(max_length = 16)
    meter_reading = models.CharField(max_length = 24)
    reading_date = models.DateField(auto_now=False, auto_now_add=True)
    # reading_date = models.DateField()


    
    
    