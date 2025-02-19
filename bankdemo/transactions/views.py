from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TransactionSerializer
from accounts.models import AccountModel
from .models import TransactionsModel
from users.permissions import IsAdminOrAccountOwner, IsAccountOwner
# Create your views here.

class TrasanctionViews(APIView):
    

    def get_permissions(self):
        
        if self.request.method in ["GET"]:
            return [permissions.IsAuthenticated(), IsAdminOrAccountOwner()]  # Restrict GET to admins
        return [IsAccountOwner()]  # Other methods are allowed for account owner
    
    def post(self, request):
       
        
        serializer = TransactionSerializer(data=request.data)
        user = request.user
        try:
            sender = AccountModel.objects.get(user=user)
        except AccountModel.DoesNotExist:
            return Response({"error": "Sender account not found."}, status=status.HTTP_400_BAD_REQUEST)

       
        try:
            amount = request.data.get('amount', 0)
        except ValueError:
            return Response({"error": "Invalid amount provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction_type= request.data.get('transaction_type')

        self.check_object_permissions(self.request, sender)

        if serializer.is_valid():

            transaction = serializer.save(sender=sender)
          
            if transaction_type == "transfer" :
                  
                  receiver = str(request.data.get('receiver'))
                  try:
                   receiver_account= AccountModel.objects.get(account_number=receiver)
                  except AccountModel.DoesNotExist:
                      return Response({"error": "receiver account not found, please confirm receiver account"}, status=status.HTTP_404_NOT_FOUND)

                  if not sender or not receiver:
                        return Response(
                            {"error": "Both sender and receiver accounts are required for a transfer."},
                            status=status.HTTP_400_BAD_REQUEST,)

                  if sender.balance < amount:
                        transaction.status= "failed"
                        transaction.save()
                        return Response({'error': 'insufficient funds for this senders account'}, 
                        status=status.HTTP_400_BAD_REQUEST)
                        
                        # carry out the transactions
                  sender.balance -= amount
                  receiver_account.balance += amount
                  # save new balance
                  sender.save()
                  receiver_account.save()

            elif transaction_type == "withdrawal":

                  if not sender:
                        return Response(
                            {"error": "Sender account is required for a withdrawal."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                
                  if sender.balance < amount:
                        
                        transaction.status="failed"
                        transaction.save()
                        return Response({'error': 'insufficient funds for this senders account'}, status=status.HTTP_400_BAD_REQUEST)
                  
                  sender.balance -= amount
                  sender.save()

            elif  transaction_type == "deposit":
                  
                  sender.balance += amount
                  sender.save()
              # Save the valid transaction data
            
            
            
            transaction.status = 'succesfull'
            transaction.save()
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
