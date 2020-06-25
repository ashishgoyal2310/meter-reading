from django.db import models
from django.conf import settings
import uuid


# Create your models here.

class UserAuthToken(models.Model):
    token = models.CharField(max_length = 64)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_token',
    )

    @staticmethod
    def generate_unique_key():
        unique_key = uuid.uuid4().hex
        return unique_key

    def __str__(self):
        return '%s %s' % (self.user, self.token)


