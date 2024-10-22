from flask import request, jsonify
from jsonschema import validate, ValidationError

"""
    Decorator to put before routes to do jsonschema API validation.
    The API returns 400 if the request is malformed

    for more info: https://json-schema.org
"""
def validate_json(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                request_data = request.get_json()
                validate(instance=request_data, schema=schema)
            except ValidationError as e:
                return jsonify({"error": f"Invalid request: {e.message}"}), 400
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

user_create_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
        "dob": {"type": "string", "format": "date-time"},
    },
    "required": ["username", "name", "last_name", "password"],
    "additionalProperties": False
}

user_update_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
        "dob": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": False
}

auth_login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
    },
    "required": ["username", "password"],
    "additionalProperties": False
}
