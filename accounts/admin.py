from django.contrib import admin
from .models import AccountModel

# Register your models here.

class AccountsAdmin(admin.ModelAdmin):
    list_display = ('id' ,'account_number', 'user', 'balance', 'account_type')
    
admin.site.register(AccountModel, AccountsAdmin)