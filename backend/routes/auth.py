import re
import bcrypt
from flask import Blueprint, request, jsonify
from utils.jwt_helper import sign_token
import models.user as user_model
import models.log as log_model
from limiter import limiter

auth_bp = Blueprint("auth", __name__)

def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per 15 minutes")
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    role = data.get("role", "user").strip()

    # Input validations
    errors = []
    if not name:
        errors.append({"field": "name", "message": "Name is required."})
    if not email:
        errors.append({"field": "email", "message": "Email is required."})
    elif not is_valid_email(email):
        errors.append({"field": "email", "message": "Invalid email address format."})
    if not password:
        errors.append({"field": "password", "message": "Password is required."})
    elif len(password) < 6:
        errors.append({"field": "password", "message": "Password must be at least 6 characters long."})
    if role not in ["admin", "user"]:
        errors.append({"field": "role", "message": "Role must be 'admin' or 'user'."})

    if errors:
        log_model.create_log(action="REGISTER_FAILURE", details=f"Validation failed during registration for email: {email}")
        return jsonify({"success": False, "message": "Validation failed.", "errors": errors}), 400

    # Check for duplicate email
    existing_user = user_model.find_by_email(email)
    if existing_user:
        log_model.create_log(action="REGISTER_FAILURE", details=f"Attempted registration with duplicate email: {email}")
        return jsonify({"success": False, "message": "Validation failed.", "errors": [{"field": "email", "message": "Email address is already in use."}]}), 400

    try:
        # Hash password
        salt = bcrypt.gensalt(rounds=10)
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        # Insert user into database
        user_id = user_model.create(name, email, password_hash, role)

        # Generate JWT
        token = sign_token({"id": user_id, "email": email, "role": role})

        # Log successful registration
        log_model.create_log(user_id=user_id, action="REGISTER_SUCCESS", details=f"User registered successfully: {email} ({role})")

        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "data": {
                "token": token,
                "user": {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "role": role
                }
            }
        }), 201

    except Exception as error:
        log_model.create_log(action="REGISTER_FAILURE", details=f"System error during registration: {str(error)}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per 15 minutes")
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    errors = []
    if not email:
        errors.append({"field": "email", "message": "Email is required."})
    elif not is_valid_email(email):
        errors.append({"field": "email", "message": "Invalid email address format."})
    if not password:
        errors.append({"field": "password", "message": "Password is required."})

    if errors:
        return jsonify({"success": False, "message": "Validation failed.", "errors": errors}), 400

    # Fetch user from DB
    user = user_model.find_by_email(email)
    if not user:
        log_model.create_log(action="LOGIN_FAILURE", details=f"Failed login attempt for non-existent email: {email}")
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    # Verify password hash
    try:
        is_match = bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8"))
        if not is_match:
            log_model.create_log(user_id=user["id"], action="LOGIN_FAILURE", details=f"Failed login attempt (incorrect password) for: {email}")
            return jsonify({"success": False, "message": "Invalid email or password."}), 401

        # Generate JWT
        token = sign_token({"id": user["id"], "email": user["email"], "role": user["role"]})

        # Log login success
        log_model.create_log(user_id=user["id"], action="LOGIN_SUCCESS", details=f"User logged in successfully: {email}")

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "data": {
                "token": token,
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }
        }), 200

    except Exception as error:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500
