from django.db import models
from accounts.models import AccountModel
from django.core.validators import MinValueValidator
# Create your models here.


class TransactionsModel(models.Model):
    Status = (('succesfull', 'Succesfull'), 
              ('pending', 'Pending'), 
              ('failed', 'Failed'))
    
    Transaction_type =(('transfer', 'Transfer'),
                       ('withdrawal', 'Withdrawal'),
                       ('deposit', 'Deposit'))


    sender=models.ForeignKey('accounts.AccountModel', on_delete=models.CASCADE,  related_name='sender', null=True, blank=True )
    receiver=models.CharField( max_length=10, null=True, blank=True )
    amount=models.FloatField(validators=[MinValueValidator(1)])
    transaction_type=models.CharField(max_length=40, choices=Transaction_type
    )
    status = models.CharField(max_length=20 ,choices=Status, null=False, blank=False ,default='pending')
    timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.Transaction_type} {self.amount}" 