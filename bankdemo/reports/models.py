from django.db import models

# Create your models here.

class  ReportsModel(models.Model):

    Report_type = (("transaction_summary", "Transaction_summary" )
                   ,( "account_summary" ,"Account_summary"))

    report_type = models.CharField(max_length=30, choices=Report_type)
    generated_by = models.ForeignKey('users.NewUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return self.report_type