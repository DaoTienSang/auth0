class Auth0SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is a logout request
        if request.path.endswith('/logout/'):
            # Clear Auth0-specific session data
            auth0_keys = [key for key in request.session.keys() if 'auth0' in key.lower()]
            for key in auth0_keys:
                del request.session[key]
            
            # Clear social auth session data
            social_keys = [key for key in request.session.keys() if 'social' in key.lower()]
            for key in social_keys:
                del request.session[key]

        response = self.get_response(request)
        return response