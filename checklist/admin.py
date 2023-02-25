from django.contrib import admin
from .models import Checklist,MemberChecklist
# Register your models here.
admin.site.register(Checklist)
admin.site.register(MemberChecklist)