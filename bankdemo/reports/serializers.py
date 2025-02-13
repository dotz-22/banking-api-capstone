from rest_framework import serializers
from .models import ReportsModel
from datetime import datetime
from accounts.models import AccountModel

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReportsModel
        fields = '__all__'



    def validate(self, attrs):
        """
        Custom validation for the report fields.
        """
        data = attrs.get('data', {})
        report_type = attrs.get('report_type')

        if not isinstance(data, dict):
            raise serializers.ValidationError({"data": "The 'data' field must be a valid JSON object."})

        if report_type == 'transaction_summary':
            if 'from' not in data or 'to' not in data:
                raise serializers.ValidationError(
                    {"data": "For 'transaction_summary', 'from' and 'to' dates are required."}
                )

            # Validate date format
            try:
                start_date = datetime.strptime(data['from'], '%Y-%m-%d')
                end_date = datetime.strptime(data['to'], '%Y-%m-%d')
                if start_date > end_date:
                    raise serializers.ValidationError(
                        {"data": "'from' date must be earlier than 'to' date."}
                    )
            except ValueError:
                raise serializers.ValidationError(
                    {"data": "'from' and 'to' must be in the format 'YYYY-MM-DD'."}
                )

        elif report_type == 'account_summary':
            if "account_number" not in data:
                raise serializers.ValidationError(
                    {"data": "For 'account_summary', 'account_number' must be provided."}
                )

            account_number = str(data['account_number']).strip()

            if len(account_number) != 10:
                raise serializers.ValidationError(
                    {"data": "Invalid account number. Account  number should be 10 digits"}
                )

            if not AccountModel.objects.filter(account_number=account_number).exists():
                raise serializers.ValidationError(
                    {"data": "Account number not found."}
                )

        return attrs

    # def validate(self, data):
    #     """
    #     General validation for the serializer.
    #     """
    #     data['data'] = self.validate_data(data['data'])
    #     return data


    # def validate_data(self, value):
    #     """
    #     Custom validation for the `data` JSONField.
    #     """
    #     if not isinstance(value, dict):
    #         raise serializers.ValidationError("The 'data' field must be a valid JSON object.")
        
    #     request_data= self.context.get("request").data if self.context.get('request') else{}
    #     report_type= request_data.get('report_type')
    #     # Validate required keys for 'transaction_summary'
    #     if report_type == 'transaction_summary':
    #         if 'from' not in value or 'to' not in value:
    #             raise serializers.ValidationError("For 'transaction_summary', 'start_date' and 'end_date' are required in 'data'.")
            
    #         # Validate the date format
    #         try:
    #             start_date = datetime.strptime(value['from'], '%Y-%m-%d')#check '%Y-%m-%d
    #             end_date = datetime.strptime(value['to'], '%Y-%m-%d')
    #             if start_date > end_date:
    #                 raise serializers.ValidationError("'start_date' must be earlier than 'end_date'.")
    #         except ValueError:
    #             raise serializers.ValidationError("'start_date' and 'end_date' must be in the format 'YYYY-MM-DD'.")

    #     if report_type == 'account_summary':
    #         if "account_number" not in value:
    #             raise serializers.ValidationError("for 'account summary', 'account number' must be provided")
    #         try: 
    #             account = value['account_number']

    #             if len (account) < 10:
    #                 raise serializers.ValidationError('incomplete account number')

    #             if not AccountModel.objects.filter(account_number=account).exists():
    #                 raise serializers.ValidationError('account number not found')
    #         except ValueError:
    #             raise serializers.ValidationError('account number must be string')

    #     # Add additional validations for other report types if needed
    #     return value
    
       
            

