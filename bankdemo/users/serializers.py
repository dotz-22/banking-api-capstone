from rest_framework import serializers
from .models import NewUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
      model = NewUser
      fields = '__all__'


    def validate(self, data):
       if data['password'] != data['password2']:
        raise serializers.ValidationError({'password': 'passwords must match'})
      
       validate_password(data['password'])
       return data
    
    def create(self, validated_data):
        try:
           user = NewUser(
            email=validated_data['email'],
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
            phone_number= validated_data['phone_number'],
            role = validated_data['role']
            
          )
           user.set_password(validated_data['password'])  # Hash the password
           user.save()
           return user
        
        except Exception as e:
           raise serializers.ValidationError({'error': str(e)})
