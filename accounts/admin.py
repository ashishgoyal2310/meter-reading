from django.contrib import admin
from accounts.models import UserAuthToken, UserForgetPassword

# Register your models here.

admin.site.register(UserAuthToken)
admin.site.register(UserForgetPassword)

