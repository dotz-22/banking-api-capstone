from django.contrib import admin
from .models import NewUser
from django.contrib.auth.models import Group
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ('id', 'email', 'first_name', 'last_name', "phone_number",'role', "is_superuser")
    search_fields=('phone_number', 'email')


admin.site.register(NewUser, CustomUserAdmin)
admin.site.unregister(Group)