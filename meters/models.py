from django.db import models
from django.conf import settings

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
    
    def __str__(self):
        return '%s %s' % (self.user, self.meter_number)