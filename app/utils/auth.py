import os
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import current_app, request, jsonify
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError


def _get_secret_key() -> str:
    """
    Prefer SECRET_KEY from environment (.env / Render / GitHub Actions),
    but fall back to Flask config if needed.
    """
    secret = os.getenv("SECRET_KEY")
    if secret:
        return secret

    # Fallback (helps if your app sets SECRET_KEY in config.py)
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError(
            "SECRET_KEY is not set. Add it to your .env and/or Render env vars."
        )
    return secret


def encode_token(customer_id: int) -> str:
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(tz=timezone.utc),
        "sub": str(customer_id),
        "type": "customer",  # helpful if you later do mechanic tokens
    }

    secret = _get_secret_key()
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
            secret = _get_secret_key()
            data = jwt.decode(token, secret, algorithms=["HS256"])

            customer_id = int(data["sub"])

            # optionally enforce token type
            if data.get("type") != "customer":
                return jsonify({"message": "Invalid token type"}), 401

        except ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except (JWTError, KeyError, ValueError, TypeError):
            return jsonify({"message": "Invalid token"}), 401

        # Pass customer_id into the route
        return f(customer_id, *args, **kwargs)

    return decorated
