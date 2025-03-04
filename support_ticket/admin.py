from django.contrib import admin
from .models import SupportModel

# Register your models here.

class SupportAdmin(admin.ModelAdmin):
    list_display =("id", "user","subject","description", "status", "created_at")

admin.site.register(SupportModel, SupportAdmin)