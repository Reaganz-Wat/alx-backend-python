from django.contrib import admin
from .models import Message, Notifications

# Register your models here.
admin.site.register(Message)
admin.site.register(Notifications)