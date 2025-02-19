from rest_framework import serializers
from .models import AccountModel

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = AccountModel
        fields = "__all__"


  
