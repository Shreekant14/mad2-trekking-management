from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.decorators import admin_required
from app.extensions import db
from app.models import Trek

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)

@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
@admin_required
def create_trek():

    data = request.get_json()

    required_fields = [
        "title",
        "location",
        "difficulty",
        "duration",
        "price",
        "description",
        "start_date",
        "end_date",
        "total_slots"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    claims = get_jwt()

    trek = Trek(
        title=data["title"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration=data["duration"],
        price=data["price"],
        description=data["description"],
        start_date=datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date(),
        end_date=datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date(),
        total_slots=data["total_slots"],
        available_slots=data["total_slots"],
        created_by=int(claims["sub"])
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully"
    }), 201

@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    data = request.get_json()

    for field in [
        "title",
        "location",
        "difficulty",
        "duration",
        "price",
        "description",
        "total_slots",
        "available_slots",
        "status"
    ]:
        if field in data:
            setattr(trek, field, data[field])

    if "start_date" in data:
        trek.start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date()

    if "end_date" in data:
        trek.end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date()

    db.session.commit()

    return jsonify({
        "message": "Trek updated successfully"
    }), 200

@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
@admin_required
def get_all_treks():

    treks = Trek.query.all()

    return jsonify([
        trek.to_dict() for trek in treks
    ]), 200

@admin_bp.route("/treks/<int:trek_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    return jsonify(trek.to_dict()), 200

@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek deleted successfully"
    }), 200