import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Auth0 configuration
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = [os.environ.get('ALGORITHM')]
API_AUDIENCE = os.environ.get('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    '''
    attempts to get the header from the request
        raises an AuthError if no header is present
    attempts to split bearer and the token
        raises an AuthError if the header is malformed
    return the token part of the header
    '''
    # get the authorization header from request
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        raise AuthError('No authorization header found', 401)
    # get the bearer token
    auth_header_splitted = auth_header.split(sep=' ')
    if auth_header_splitted[0].lower() != 'bearer':
        raise AuthError('Authorization header malformed', 401)
    try:
        token = auth_header_splitted[1]
        return token
    except Exception:
        raise AuthError('Authorization header malformed', 401)


def check_permissions(permission, payload: dict):
    '''
    @INPUTS
        permission: string permission (i.e. 'patch:actors')
        payload: decoded jwt payload

    raises an AuthError if permissions are not included in the payload
    raises an AuthError if permission string is not in the payload permissions
    return true otherwise
    '''
    if 'permissions' not in payload:
        raise AuthError('no permissions list present', 403)
    if permission not in payload['permissions']:
        raise AuthError(
            'you don\'t have enough permissions to perform this action', 403)
    return True


def verify_decode_jwt(token):
    '''
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    verifies the token using Auth0 /.well-known/jwks.json
    decodes the payload from the token
    validates the claims
    return the decoded payload
    '''
    try:
        # get the header part of the submitted token
        header = jwt.get_unverified_header(token)
        # check if the header has key id
        if 'kid' not in header:
            raise AuthError('malform token', 401)
        # get authorization keys from auth0
        json_signature_data = urlopen(
            'https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).read()
        data = json.loads(json_signature_data)
        # look for the required kid
        rsa_key_list = list(
            filter(lambda x: x['kid'] == header['kid'], data['keys']))
        if len(rsa_key_list) < 1:
            # raise an error if no key with this kid
            raise AuthError('kid not valid', 401)
        rsa_key = rsa_key_list[0]
        # decode token
        payload = jwt.decode(
            token,
            rsa_key,
            ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://{}/'.format(AUTH0_DOMAIN)
        )
        return payload
    # possible exceptions
    except jwt.JWTClaimsError:
        raise AuthError('invalid claims', 401)
    except jwt.ExpiredSignatureError:
        raise AuthError('expired token provided', 401)
    except AuthError as e:
        raise AuthError(e.message, e.status_code)
    except Exception as e:
        raise AuthError('Authentication failed',  401)


def requires_auth(permission=''):
    '''
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt  to decode the jwt
    uses the check_permissions to validate claims and check for permission
    passes the decoded payload to the decorated method
    return decorator
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            _request_ctx_stack.top.current_user = payload
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
