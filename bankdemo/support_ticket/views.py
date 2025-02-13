from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import SupportSerializer
from accounts.models import AccountModel
from .models import SupportModel
from users.permissions import IsAdminOrAccountOwner, IsCustomer, IsAdminUser

# Create your views here.

class SupportView(APIView):
    def get_permissions(self):
    
        if self.request.method in ["GET"]:
            return [permissions.IsAuthenticated(), IsAdminOrAccountOwner()]  # Restrict GET to admins
        if self.request.method == "PATCH":
            return [IsAdminUser()]
        return [IsCustomer()]  # Other methods are allowed for any authen

        

    def post (self, request):
        serialized = SupportSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response ("ticket created succesfully", status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, request, id=None):
        if id :
            try:
              self.check_object_permissions(self.request, support_ticket)
              support_ticket = SupportModel.objects.get(id=id)
              serialized= SupportSerializer(support_ticket)
              return Response({"ticket": serialized.data})
            except SupportModel.DoesNotExist:
                return Response("ticket not found", status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.role == 'admin':  
            return Response({'error': 'You do not have permission to view all tickets'}, status=status.HTTP_403_FORBIDDEN)
        support_tickets = SupportModel.objects.all()
        serialized2= SupportSerializer(support_tickets, many= True)
        
        return Response({"tickets": serialized2.data})
    
    def patch (self, request, id):
        data = request.data
        try:
            ticket = SupportModel.objects.get(id=id)
        except SupportModel.DoesNotExist:
            return Response ("ticket deos not exist", status= status.HTTP_204_NO_CONTENT)
        
        serialized = SupportSerializer(ticket, data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response ("ticket updated successfully", status=status.HTTP_202_ACCEPTED)
        