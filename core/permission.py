from rest_framework.permissions import BasePermission
from .models import Account

class AuthUser(BasePermission):
    def has_permission(self, request, view):
        
        token = request.headers.get('CL-X-TOKEN')

        if not token:
            return False 

        try:
            account = Account.objects.get(secret_token=token)
            request.account = account 
            return True 
        except Account.DoesNotExist:
            return False  