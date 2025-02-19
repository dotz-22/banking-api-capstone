from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import AccountSerializer
from .models import AccountModel
from users.permissions import IsAdminOrAccountOwner, IsCustomer,IsAdminUser

# Create your views here.



class AccountsView(APIView):
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        
        if self.request.method in ["GET"]:
            return [permissions.IsAuthenticated(), IsAdminOrAccountOwner()]  # Restrict GET to admins
        
        return [IsAdminUser()]  # Other methods are allowed for any authen

    def post(self, request):
        
        Serialized_Data = AccountSerializer( data = request.data)
        if Serialized_Data.is_valid():
            # user =request.user
            # Serialized_Data.validated_data['user']= user
            Serialized_Data.save()
            return Response ('account created successfully', status= status.HTTP_201_CREATED)
        else:
            return Response(Serialized_Data.errors, status= status.HTTP_206_PARTIAL_CONTENT)
        

    def get(self, request, id=None):
        if id:
    
            try:
                account = AccountModel.objects.get(id=id)
                self.check_object_permissions(self.request, account)
                serialized1 = AccountSerializer(account)
                return Response({"message": "here are the account details", "details" : serialized1.data })
            
            except AccountModel.DoesNotExist :
                return Response('account not in database', status=status.HTTP_404_NOT_FOUND)
            
        if not request.user.role == 'admin':  
            return Response({'error': 'You do not have permission to view all accounts'}, status=status.HTTP_403_FORBIDDEN)
        accounts = AccountModel.objects.all()
       
       
        serialized = AccountSerializer(accounts, many=True)

        return Response({"message": "accounts Get request successful", "data" : serialized.data})
    

    def patch(self, request, id):
        data = request.data
        try :
            account = AccountModel.objects.get(id=id)
        except AccountModel.DoesNotExist:
            return Response ("account deos not exist", status= status.HTTP_204_NO_CONTENT)
        
        serialized = AccountSerializer(account, data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response ("account updated successfully", status=status.HTTP_202_ACCEPTED)
        

    def delete(self, request, id):
        
        try:
            account = AccountModel.objects.get(id=id)
            
        except AccountModel.DoesNotExist:
            return Response ("account deos not exist", status= status.HTTP_204_NO_CONTENT)
        
        account.delete()
        
        return Response ("deleted successfully") 
    