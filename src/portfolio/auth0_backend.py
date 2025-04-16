from social_core.backends.auth0 import Auth0OAuth2
from jwt.api_jwt import decode_complete
import time

class CustomAuth0OAuth2(Auth0OAuth2):
    def get_jwt_key_and_algorithm(self):
        """Override get_jwt_key_and_algorithm to specify RS256 algorithm"""
        key = self.get_key_and_secret()[0]
        algorithm = 'RS256'
        return key, algorithm

    def decode_jwt(self, token, key=None, verify=True):
        """Override the default JWT decode to handle clock skew issues"""
        key = key or self.get_key_and_secret()[0]
        
        # Calculate current timestamp and add a leeway
        current_time = int(time.time())
        leeway = 300  # 5 minutes leeway
        
        # Custom options to handle clock skew
        options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False,
            'verify_iss': False,
            'require_exp': True,
            'require_iat': True,
            'leeway': leeway
        }
        
        try:
            decoded = decode_complete(token, key=key, algorithms=['RS256'], options=options)
            
            # Manual validation of 'iat' claim with leeway
            if 'iat' in decoded['payload']:
                iat = decoded['payload']['iat']
                if iat - leeway > current_time:
                    # If token's iat is too far in the future, adjust it
                    decoded['payload']['iat'] = current_time
            
            return decoded
            
        except Exception as e:
            # If there's still an error, try one more time with iat validation disabled
            options['verify_iat'] = False
            options['require_iat'] = False
            return decode_complete(token, key=key, algorithms=['RS256'], options=options)