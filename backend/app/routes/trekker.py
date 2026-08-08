from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import trekker_required
from app.extensions import db
from app.models import Trek, Booking

trekker_bp = Blueprint(
    "trekker",
    __name__,
    url_prefix="/api/trekker"
)


@trekker_bp.route("/treks", methods=["GET"])
@jwt_required()
@trekker_required
def get_available_treks():

    treks = Trek.query.filter_by(status="UPCOMING").all()

    return jsonify([
        trek.to_dict() for trek in treks
    ]), 200

# Cheack available trek

@trekker_bp.route("/bookings", methods=["POST"])
@jwt_required()
@trekker_required
def book_trek():

    data = request.get_json()

    if "trek_id" not in data:
        return jsonify({
            "message": "trek_id is required"
        }), 400

    trek = Trek.query.get(data["trek_id"])

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    if trek.status != "UPCOMING":
        return jsonify({
            "message": "Bookings are closed for this trek"
        }), 400

    people = data.get("number_of_people", 1)

    if trek.available_slots < people:
        return jsonify({
            "message": "Not enough slots available"
        }), 400

    booking = Booking(
        user_id=int(get_jwt_identity()),
        trek_id=trek.id,
        number_of_people=people,
        status="CONFIRMED"
    )

    trek.available_slots -= people

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking successful"
    }), 201

# Show all bookings of the trekker

@trekker_bp.route("/bookings", methods=["GET"])
@jwt_required()
@trekker_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=int(get_jwt_identity())
    ).all()

    result = []

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        result.append({
            "id": booking.id,
            "trek_id": trek.id if trek else None,
            "trek_title": trek.title if trek else "Unknown",
            "number_of_people": booking.number_of_people,
            "status": booking.status,
            "booked_at": booking.booked_at.isoformat()
        })

    return jsonify(result), 200

# Cancel a booking of the trekker

@trekker_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
@trekker_required
def cancel_booking(booking_id):

    booking = Booking.query.filter_by(
        id=booking_id,
        user_id=int(get_jwt_identity())
    ).first()

    if not booking:
        return jsonify({
            "message": "Booking not found"
        }), 404

    if booking.status == "CANCELLED":
        return jsonify({
            "message": "Booking already cancelled"
        }), 400

    trek = Trek.query.get(booking.trek_id)

    if trek:
        trek.available_slots += booking.number_of_people

    booking.status = "CANCELLED"

    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully"
    }), 200

# Trekker Dashboard

@trekker_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@trekker_required
def trekker_dashboard():

    user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    total = len(bookings)

    confirmed = 0
    cancelled = 0

    for booking in bookings:

        if booking.status == "CONFIRMED":
            confirmed += 1

        elif booking.status == "CANCELLED":
            cancelled += 1

    return jsonify({
        "total_bookings": total,
        "confirmed": confirmed,
        "cancelled": cancelled
    }), 200