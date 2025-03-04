from rest_framework import serializers
from .models import TransactionsModel

class TransactionSerializer(serializers.ModelSerializer):


    class Meta:
        model= TransactionsModel
        fields = '__all__'

        def validate(self, data):
            transaction_type = data.get('transaction_type')
            amount = data.get("amount")
            

            if transaction_type == 'transfer':
                receiver_account = str(data.get('receiver'))
                if not  receiver_account:
                    raise serializers.ValidationError(" receiver accounts are required for transfers.")
                
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0.")
            

            return data
        
       