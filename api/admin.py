from django.contrib import admin
from .models import Album, Picture
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Album)
admin.site.register(Picture)

TokenAdmin.raw_id_fields = ['user']