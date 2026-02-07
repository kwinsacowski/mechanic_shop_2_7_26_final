from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import current_app, jsonify, request
from jose import jwt
import jose


def encode_token(customer_id: int) -> str:
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(tz=timezone.utc),
        "sub": str(customer_id),
        "type": "customer"  # helpful if you later do mechanic tokens
    }
    secret = current_app.config["SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        # Expect: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Authorization header must be 'Bearer <token>'"}), 401

        token = parts[1]
        try:
            secret = current_app.config["SECRET_KEY"]
            data = jwt.decode(token, secret, algorithms=["HS256"])

            customer_id = int(data["sub"])
            # optionally enforce type
            if data.get("type") != "customer":
                return jsonify({"message": "Invalid token type"}), 401

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except (jose.exceptions.JWTError, KeyError, ValueError):
            return jsonify({"message": "Invalid token"}), 401

        # Pass customer_id into the route
        return f(customer_id, *args, **kwargs)

    return decorated
