from datetime import datetime
from transactions.models import TransactionsModel
from .serializers import ReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdminUser
from accounts.models import AccountModel
from .models import ReportsModel


class ReportListView(APIView):
    permission_classes = [IsAdminUser]
   

    def post(self, request):
        user = request.user
        serializer = ReportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(generated_by=user)
            # Generate report dynamically based on report_type and data
            report_type = serializer.validated_data['report_type']
            report_data = serializer.validated_data['data']

            if report_type == 'transaction_summary':

                start_date_str = report_data.get('from')
                end_date_str = report_data.get('to')
                # Fetch transactions between start_date and end_date
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                transactions = TransactionsModel.objects.filter(
                    timestamp__range=(start_date, end_date)
                )
                # Add details to the data field
                report_data['total_transactions'] = transactions.count()
                report_data['total_value'] = sum(t.amount for t in transactions)

            # Save the report with updated data
            if report_type == 'account_summary':
                
                account_number = report_data.get("account_number")
                # account= AccountModel.objects.get(account_number=account_number)
                transactions = TransactionsModel.objects.filter(
                    sender__account_number = account_number)|TransactionsModel.objects.filter(
                        receiver = account_number)
                #

                report_data['total_transactions'] = transactions.count()
                # report_data['transactions'] = transactions


            serializer.save(generated_by=request.user, data=report_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get (self, requets, id=None):
        if id :
            try:
                report = ReportsModel.objects.get(id =id)

                serialized_data = ReportSerializer(report)
                return Response({"report" : serialized_data.data})

            except ReportsModel.DoesNotExist:
                return Response({"report not found !!"}, status=status.HTTP_404_NOT_FOUND)
            
        reports = ReportsModel.objects.all()
        serialized2 = ReportSerializer(reports, many= True)
        
        return Response({"reports": serialized2.data})