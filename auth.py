import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'capstone-fsndp.us.auth0.com'
AUTH0_CLIENT_ID = 'moviescast'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'moviescast'


'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
Implement get_token_auth_header() method
'''


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError('No Authorization', 401)

    head_authorization = auth.split()

    if len(head_authorization) != 2:
        raise AuthError('Invalid Authorization', 401)
    elif head_authorization[0].lower() != 'bearer':
        raise AuthError('Invalid Authorization', 401)

    return head_authorization[1]

'''
Implement check_permissions(permission, payload) method
'''

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('No permissions found', 401)

    if permission not in payload['permissions']:
        raise AuthError('Bad permissions', 401)

    return True


'''
Implement verify_decode_jwt(token) method
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('Invalid Authorization', 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError('Signature is Expired', 401)

        except jwt.JWTClaimsError:
            raise AuthError('Invalid claims', 401)
        except Exception as e:
            raise AuthError('Unable to parse authentication token.', 400)
    raise AuthError('Key not found', 400)

'''
Implement @requires_auth(permission) decorator method
'''

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator