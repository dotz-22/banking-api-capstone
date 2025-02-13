from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        admin = request.user.is_authenticated and request.user.role == 'admin' 
        return admin

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
       customer= request.user.is_authenticated and request.user.role == 'customer' 
       return customer
    



class IsAdminOrAccountOwner(BasePermission):
    """
    Custom permission to allow admins or the owner of the account to perform actions.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        return True  # If the user is authenticated, proceed to object-level check

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is an admin or the owner of the account.
        """
        # Allow if the user is an admin or the owner of the account
        if request.user.role == "admin" or request.user == obj.user:
            return True

        return False
    
class IsAccountOwner(BasePermission):
    """
    Custom permission to allow only the owner of the account to perform actions.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        return True  # If the user is authenticated, proceed to object-level check

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is an admin or the owner of the account.
        """
        # Allow if the user is an admin or the owner of the account
        if request.user == obj.user:
            return True

        return False