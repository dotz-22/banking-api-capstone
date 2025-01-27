from rest_framework import serializers
from .models import TransactionsModel

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= TransactionsModel
        fields = '__all__'

        def validate(self, data):
            transaction_type = data.get('transaction_type')
            sender_account = data.get('sender')
            receiver_account = data.get('receiver')

            if transaction_type == 'withdrawal' and receiver_account is not None:
                raise serializers.ValidationError("Receiver account must be null for withdrawal transactions.")

            if transaction_type == 'deposit' and sender_account is not None:
                raise serializers.ValidationError("Sender account must be null for deposit transactions.")

            if transaction_type == 'transfer':
                if not sender_account or not receiver_account:
                    raise serializers.ValidationError("Both sender and receiver accounts are required for transfers.")

            return data