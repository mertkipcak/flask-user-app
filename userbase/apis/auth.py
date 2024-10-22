from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from userbase.models.user import User
from userbase.utils.api_schemas import validate_json, auth_login_schema

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
@validate_json(auth_login_schema)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id, additional_claims={'user_id': user.id})
    return jsonify({'access_token': access_token}), 200


@auth_bp.route('/admin', methods=['POST'])
def admin_login():
    provided_secret = request.args.get('secret')

    from userbase.utils.config import CONFIG
    expected_secret = CONFIG.get('admin_secret')

    if provided_secret != expected_secret:
        return jsonify({'error': 'Invalid or missing secret key'}), 403

    access_token = create_access_token(identity='admin', additional_claims={'is_admin': True})
    return jsonify({'access_token': access_token}), 200