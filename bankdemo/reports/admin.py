from django.contrib import admin
from .models import ReportsModel
# Register your models here.


class ReportsAdmin(admin.ModelAdmin):
    list_display=["id", "report_type","generated_by", "created_at" ]

admin.site.register(ReportsModel, ReportsAdmin)