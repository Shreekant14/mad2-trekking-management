from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "ADMIN":
            return jsonify({
                "message": "Admin access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper

def staff_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "STAFF":
            return jsonify({
                "message": "Staff access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def trekker_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "TREKKER":
            return jsonify({
                "message": "Trekker access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper