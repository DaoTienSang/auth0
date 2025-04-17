class Auth0SessionMiddleware:
    """Middleware to handle Auth0 session issues"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear any problematic session data that might cause issues with Auth0
        if request.path.startswith('/login/auth0/'):
            # Keep only minimal data in session for Auth0
            keys_to_keep = ['_auth_user_id', '_auth_user_backend', '_auth_user_hash']
            for key in list(request.session.keys()):
                if key not in keys_to_keep and not key.startswith('_auth_user'):
                    del request.session[key]
            # Ensure session is saved immediately
            request.session.modified = True
            
        response = self.get_response(request)
        return response