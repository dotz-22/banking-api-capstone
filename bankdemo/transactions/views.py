from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TransactionSerializer
from accounts.models import AccountModel
from .models import TransactionsModel
from users.permissions import IsAdminOrAccountOwner, IsCustomer, IsAdminUser, IsAccountOwner
# Create your views here.

class TrasanctionViews(APIView):
    

    def get_permissions(self):
        
        if self.request.method in ["GET"]:
            return [permissions.IsAuthenticated(), IsAdminOrAccountOwner()]  # Restrict GET to admins
        return [IsAccountOwner()]  # Other methods are allowed for any authen
    
    def post(self, request):
       
        
        serializer = TransactionSerializer(data=request.data)

        amount= request.data.get('amount')
        transaction_type= request.data.get('transaction_type')
        sender= request.data.get('sender')
        receiver = request.data.get('receiver')
        

        account = AccountModel.objects.get(id=sender)
        
        self.check_object_permissions(self.request, account)

        if serializer.is_valid():
          
            if transaction_type == "transfer" :

                  if not sender or not receiver:
                        return Response(
                            {"error": "Both sender and receiver accounts are required for a transfer."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                  sender_account= AccountModel.objects.get(id=sender)
                  receiver_account= AccountModel.objects.get(id=receiver)

                 
            
                  if sender_account.balance < amount:
                        return Response({'error': 'insufficient funds for this senders account'}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # carry out the transactions
                  sender_account.balance -= amount
                  receiver_account.balance += amount
                  # save new balance
                  sender_account.save()
                  receiver_account.save()

            elif transaction_type == "withdrawal":

                  if not sender:
                        return Response(
                            {"error": "Sender account is required for a withdrawal."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                  sender_account= AccountModel.objects.get(id=sender)
        
                
                  if sender_account.balance < amount:
                        return Response({'error': 'insufficient funds for this senders account'}, status=status.HTTP_400_BAD_REQUEST)
                  
                  sender_account.balance -= amount
                 
                  sender_account.save()

            elif  transaction_type == "deposit":
                  
                  receiver_account= AccountModel.objects.get(id=receiver)

                  receiver_account.balance += amount
                 

                  receiver_account.save()
              # Save the valid transaction data
            
            receipt = serializer.save()
            receipt.status = 'succesfull'
            receipt.save()
            return Response({"transaction_type":transaction_type , "message":' successful'} ,status=status.HTTP_201_CREATED)
      
        # Return errors if serializer validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, request, id=None):
      if id:
            try:
             transaction1 = TransactionsModel.objects.get(id=id)
             account1 =transaction1.sender
             account2 =transaction1.receiver
             self.check_object_permissions(self.request, account1 or account2)

             serialized = TransactionSerializer(transaction1)
             return Response({"message": "here are details about", "details" : serialized.data })
            except AccountModel.DoesNotExist :
                return Response('transaction not in database', status=status.HTTP_404_NOT_FOUND)
         
      if not request.user.role == 'admin':  
            return Response({'error': 'You do not have permission to view all transactions'}, status=status.HTTP_403_FORBIDDEN)
      transactions = TransactionsModel.objects.all()
      serializer = TransactionSerializer(transactions, many=True)
      return Response({"message": "accounts Get request successful", "data" : serializer.data})
