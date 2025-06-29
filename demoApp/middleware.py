from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class JSONWebTokenMiddleware(MiddlewareMixin):
    """
    Middleware for authenticating with JSON Web Tokens.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
        
    def process_request(self, request):
        """
        Process the request to authenticate using JWT.
        """
        # Skip authentication for paths that don't need it
        exempt_paths = getattr(settings, 'JWT_EXEMPT_PATHS', [])
        current_path = request.path_info
        
        if any(current_path.startswith(path) for path in exempt_paths):
            return None
            
        # Check for authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None  # Let the request continue to views that might handle unauthenticated requests
        
        try:
            # JWT authentication process
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(auth_header.split(' ')[1])
            user = jwt_auth.get_user(validated_token)
            request.user = user
        except Exception as e:
            # If authentication fails, you can either return a response here or let the view handle it
            return None
            
        return None  # Continue processing the request