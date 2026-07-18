import functools
# pyrefly: ignore [missing-import]
from flask import request, jsonify, g
# pyrefly: ignore [missing-import]
import jwt
from utils.jwt_helper import verify_token

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                
        if not token:
            return jsonify({
                "success": False,
                "message": "Access denied. No authentication token provided."
            }), 401
            
        try:
            # Decode and verify the token
            decoded_user = verify_token(token)
            # Store user info in Flask global request context
            g.user = decoded_user
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "message": "Invalid or expired authentication token."
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "message": "Invalid or expired authentication token."
            }), 401
        except Exception:
            return jsonify({
                "success": False,
                "message": "An error occurred during authentication."
            }), 401
            
        return f(*args, **kwargs)
    return decorated

def roles_accepted(*allowed_roles):
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            # Check if user is logged in and role matches
            if not hasattr(g, "user") or g.user.get("role") not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Forbidden. You do not have permission to perform this action."
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

