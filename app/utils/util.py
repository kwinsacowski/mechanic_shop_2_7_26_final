from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import jsonify, request
from jose import jwt
import jose

def encode_token(customer_id):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1), # Token expires in 1 hour
        "iat": datetime.now(tz=timezone.utc), # Issued at time
        "sub": str(customer_id) # Subject of the token, typically the customer ID
    }
    token = currnt_app.config["SECRET_KEY"]
    return jwt.encode(payload, token, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Look for the token in the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['sub']  # Fetch the user ID
            
        except jose.exceptions.ExpiredSignatureError:
             return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
             return jsonify({'message': 'Invalid token!'}), 401

        return f(user_id, *args, **kwargs)

    return decorated