from django.contrib import admin
from .models import OTP, User
from django.contrib.auth.models import Permission

# Register your models here. 
admin.site.register([OTP, Permission, User])
