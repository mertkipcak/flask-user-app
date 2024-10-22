from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from userbase.utils.auth import admin_only, user_or_admin_required
from userbase.utils.db import db
from userbase.models.user import User
from userbase.utils.api_schemas import validate_json, user_create_schema, user_update_schema

users_bp = Blueprint('user_bp', __name__)


@users_bp.route('/', methods=['GET'])
@admin_only
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200


@users_bp.route('/', methods=['POST'])
@validate_json(user_create_schema)
def create_user():
    data = request.get_json()

    # Check if a user with the same username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the user's password before saving it
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create a new User object
    new_user = User(
        username=data['username'],
        password=hashed_password,
        name=data['name'],
        last_name=data['last_name'],
        dob=data.get('dob')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

    return jsonify({'id': new_user.id, 'name': new_user.name}), 201


@users_bp.route('/<int:user_id>', methods=['GET'])
@user_or_admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'last_name': user.last_name,
        'dob': user.dob
    }), 200


@users_bp.route('/<int:user_id>', methods=['PUT'])
@user_or_admin_required
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update user details
    user.name = data.get('name', user.name)
    user.last_name = data.get('last_name', user.last_name)
    user.dob = data.get('dob', user.dob)
    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@user_or_admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user deleted'}), 200
    else:
        return jsonify({'error': 'user not found'}), 404