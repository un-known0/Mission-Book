from django.contrib import admin
from . import models
from django import forms
from django.contrib.auth.admin import UserAdmin




admin.site.register(models.Member)
admin.site.register(models.Title)
admin.site.register(models.Graduation)
