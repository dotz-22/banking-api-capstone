from django.db import models

# Create your models here.

class AccountModel(models.Model):
    ACCOUNT_TYPE=(('checking','Checking'),( 'savings', 'Savings'))

    user = models.OneToOneField('users.NewUser', on_delete=models.CASCADE) 
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.FloatField(default=0.00)
    account_type = models.CharField( max_length=40, choices=ACCOUNT_TYPE, blank=False, null=False,)
    created_at = models.CharField(max_length=120)

    def __str__(self):
         return self.account_number


{
"report_type": "account_summary",
"generated_by": 7,
"data":{
     "account_number": "11111111111"
  
}

 }

{
"report_type": "transaction_summary",
"generated_by": 7,
"data":{
    "from": "2025-01-01",
    "to":"2025-02-02"
}

 }