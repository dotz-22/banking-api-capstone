from django.contrib import admin
from .models import TransactionsModel

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display=["id",'sender', "receiver", "transaction_type", "status", "amount", "timestamp"]

admin.site.register(TransactionsModel, TransactionAdmin)