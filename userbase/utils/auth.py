from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps

def user_or_admin_required(f):
    """Require valid JWT token for either a user or an admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        token_user_id = claims.get('user_id')
        route_user_id = kwargs.get('user_id')

        # Allow access if token belongs to the correct user or is an admin
        if claims.get('is_admin') or (token_user_id and token_user_id == route_user_id):
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized access'}), 403

    return wrapper


def admin_only(f):
    """Decorator to require an admin token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        user_id = get_jwt_identity()

        # Allow access if the user is admin or the token belongs to the specific user
        if claims.get('is_admin'):
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized access'}), 403

    return wrapper
