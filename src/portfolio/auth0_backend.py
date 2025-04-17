from social_core.backends.auth0 import Auth0OAuth2
import requests
import json
from jose import jwt
from urllib.request import urlopen

class CustomAuth0OAuth2(Auth0OAuth2):
    def get_user_details(self, response):
        details = super().get_user_details(response)
        return details

    def user_data(self, access_token, *args, **kwargs):
        """Get user data from Auth0 userinfo endpoint"""
        url = f'https://{self.setting("DOMAIN")}/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            return self.get_json(url, headers=headers)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                # Token expired or invalid
                return None
            raise

    def validate_and_return_id_token(self, id_token, access_token):
        """
        Validate the JWT token without using cryptography's PEM loader
        """
        # Get the key id from the JWT token
        key_id = jwt.get_unverified_header(id_token).get('kid')
        
        # If there's no key ID, we can't find the right key
        if not key_id:
            return {}
            
        # Get the public keys from Auth0
        jwks_url = f'https://{self.setting("DOMAIN")}/.well-known/jwks.json'
        try:
            jwks = json.loads(urlopen(jwks_url).read())
            # Find the key that matches the key ID in the JWT
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == key_id:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break
            
            if not rsa_key:
                # No matching key found
                return {}
                
            # Decode the token using the public key
            options = {
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': False,
                'verify_aud': False,
                'verify_iss': False,
                'require_exp': False,
                'require_iat': False,
                'leeway': 600  # 10 minutes leeway
            }
            
            payload = jwt.decode(
                id_token,
                rsa_key,
                algorithms=['RS256'],
                options=options
            )
            
            return payload
            
        except Exception:
            # Any error in validation should result in returning an empty dict
            return {}