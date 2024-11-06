from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from .models import User
import re

class CookieAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if re.match(r'^/admin/', request.path):
            return 
        
        username = request.COOKIES.get('user_id')
        role = request.COOKIES.get('role')

        if username and role:
            try:
                user = User.objects.get(user_id=username, role=role)
                request.user = user  # Attach the user to the request
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None  # Set to None if cookie is not present or invalid