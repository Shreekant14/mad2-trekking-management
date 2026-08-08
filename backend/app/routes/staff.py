from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import staff_required
from app.models import Trek, User, StaffAssignment, Booking

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/api/staff"
)

# Get all treks assigned to the staff member

@staff_bp.route("/my-treks", methods=["GET"])
@jwt_required()
@staff_required
def my_treks():

    staff_id = int(get_jwt_identity())

    assignments = StaffAssignment.query.filter_by(
        staff_id=staff_id
    ).all()

    result = []

    for assignment in assignments:

        trek = Trek.query.get(assignment.trek_id)

        if trek:
            result.append(trek.to_dict())

    return jsonify(result), 200

# Get participants List for a specific trek assigned to the staff member

@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
@staff_required
def participants(trek_id):

    staff_id = int(get_jwt_identity())

    assignment = StaffAssignment.query.filter_by(
        staff_id=staff_id,
        trek_id=trek_id
    ).first()

    if not assignment:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    bookings = Booking.query.filter_by(
        trek_id=trek_id,
        status="CONFIRMED"
    ).all()

    result = []

    for booking in bookings:

        user = User.query.get(booking.user_id)

        if user:
            result.append({
                "booking_id": booking.id,
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "people": booking.number_of_people
            })

    return jsonify(result), 200

# Staff Dashboard

@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@staff_required
def staff_dashboard():

    staff_id = int(get_jwt_identity())

    assignments = StaffAssignment.query.filter_by(
        staff_id=staff_id
    ).all()

    assigned_treks = len(assignments)

    upcoming = 0
    completed = 0

    for assignment in assignments:

        trek = Trek.query.get(assignment.trek_id)

        if trek:

            if trek.status == "UPCOMING":
                upcoming += 1

            elif trek.status == "COMPLETED":
                completed += 1

    return jsonify({
        "assigned_treks": assigned_treks,
        "upcoming_treks": upcoming,
        "completed_treks": completed
    }), 200