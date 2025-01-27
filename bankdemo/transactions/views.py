from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TransactionSerializer
from accounts.models import AccountModel
from .models import TransactionsModel

# Create your views here.

class TrasanctionViews(APIView):
    

    
    def post(self, request):
        # Pass `request.data` to the serializer
        
        serializer = TransactionSerializer(data=request.data)

        amount= request.data.get('amount')
        transaction_type= request.data.get('transaction_type')
        sender_id= request.data.get('sender')
        receiver_id = request.data.get('receiver')
       
        
        if serializer.is_valid():
          
            if transaction_type == "transfer" :

                  if not sender_id or not receiver_id:
                        return Response(
                            {"error": "Both sender and receiver accounts are required for a transfer."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                  sender_account= AccountModel.objects.get(id=sender_id)
                  receiver_account= AccountModel.objects.get(id=receiver_id)
            
                  if sender_account.balance < amount:
                        return Response({'error': 'insufficient funds for this senders account'}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # carry out the transactions
                  sender_account.balance -= amount
                  receiver_account.balance += amount
                  # save new balance
                  sender_account.save()
                  receiver_account.save()

            elif transaction_type == "withdrawal":

                  if not sender_id:
                        return Response(
                            {"error": "Sender account is required for a withdrawal."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                  sender_account= AccountModel.objects.get(id=sender_id)
        
                
                  if sender_account.balance < amount:
                        return Response({'error': 'insufficient funds for this senders account'}, status=status.HTTP_400_BAD_REQUEST)
                  
                  sender_account.balance -= amount
                 
                  sender_account.save()

            elif  transaction_type == "deposit":
                  
                  receiver_account= AccountModel.objects.get(id=receiver_id)

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
             serialized = TransactionSerializer(transaction1)
             return Response({"message": "here are details about", "details" : serialized.data })
            except AccountModel.DoesNotExist :
                return Response('book not in database', status=status.HTTP_404_NOT_FOUND)
         

      transactions = TransactionsModel.objects.all()
      serializer = TransactionSerializer(transactions, many=True)
      return Response({"message": "accounts Get request successful", "data" : serializer.data})
