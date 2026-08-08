from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func
from app.decorators import admin_required
from app.extensions import db
from app.models import Trek, User, StaffAssignment, Booking

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)

# Admin Routes

# Trek Routes

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

# User Routes

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():

    users = User.query.all()

    return jsonify([
        user.to_dict() for user in users
    ]), 200

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user(user_id):

    user = User.query.get_or_404(user_id)

    return jsonify(user.to_dict()), 200

@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):

    user = User.query.get_or_404(user_id)

    data = request.get_json()

    if "is_active" in data:
        user.is_active = data["is_active"]

    db.session.commit()

    return jsonify({
        "message": "User updated successfully"
    }), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return jsonify({
        "message": "User deleted successfully"
    }), 200

# Staff Routes
# Create a new staff member

@admin_bp.route("/staff", methods=["POST"])
@jwt_required()
@admin_required
def create_staff():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    staff = User(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        role="STAFF",
        is_active=True
    )

    staff.set_password(data["password"])
    db.session.add(staff)
    db.session.commit()

    return jsonify({
        "message": "Staff created successfully"
    }), 201

# Get all staff members

@admin_bp.route("/staff", methods=["GET"])
@jwt_required()
@admin_required
def get_all_staff():

    staff_members = User.query.filter_by(role="STAFF").all()

    return jsonify([
        staff.to_dict() for staff in staff_members
    ]), 200

# Update a staff member's details

@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_staff(staff_id):

    staff = User.query.filter_by(
        id=staff_id,
        role="STAFF"
    ).first_or_404()

    data = request.get_json()

    if "full_name" in data:
        staff.full_name = data["full_name"]

    if "phone" in data:
        staff.phone = data["phone"]

    if "email" in data:
        existing = User.query.filter(
            User.email == data["email"],
            User.id != staff_id
        ).first()

        if existing:
            return jsonify({
                "message": "Email already exists"
            }), 400

        staff.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Staff updated successfully"
    }), 200

# Update a staff member's status (active/inactive)

@admin_bp.route("/staff/<int:staff_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def update_staff_status(staff_id):

    staff = User.query.filter_by(
        id=staff_id,
        role="STAFF"
    ).first_or_404()

    data = request.get_json()

    if "is_active" not in data:
        return jsonify({
            "message": "is_active field is required"
        }), 400

    staff.is_active = data["is_active"]

    db.session.commit()

    return jsonify({
        "message": "Staff status updated successfully",
        "is_active": staff.is_active
    }), 200

# Assignment Routes

# Assign a staff member to a trek

@admin_bp.route("/assignments", methods=["POST"])
@jwt_required()
@admin_required
def assign_staff():

    data = request.get_json()

    required_fields = ["staff_id", "trek_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    staff = User.query.filter_by(
        id=data["staff_id"],
        role="STAFF"
    ).first()

    if not staff:
        return jsonify({
            "message": "Invalid staff member"
        }), 404

    trek = Trek.query.get(data["trek_id"])

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    existing = StaffAssignment.query.filter_by(
        staff_id=data["staff_id"],
        trek_id=data["trek_id"]
    ).first()

    if existing:
        return jsonify({
            "message": "Staff already assigned to this trek"
        }), 400

    assignment = StaffAssignment(
        staff_id=data["staff_id"],
        trek_id=data["trek_id"]
    )

    db.session.add(assignment)
    db.session.commit()

    return jsonify({
        "message": "Staff assigned successfully"
    }), 201

# Get all assignments

@admin_bp.route("/assignments", methods=["GET"])
@jwt_required()
@admin_required
def get_assignments():

    assignments = StaffAssignment.query.all()

    result = []

    for assignment in assignments:

        staff = User.query.get(assignment.staff_id)
        trek = Trek.query.get(assignment.trek_id)

        result.append({
            "id": assignment.id,
            "staff_id": staff.id,
            "staff_name": staff.full_name,
            "trek_id": trek.id,
            "trek_title": trek.title,
            "assigned_on": assignment.assigned_on.isoformat()
        })

    return jsonify(result), 200

# Get assignments for a specific trek

@admin_bp.route("/treks/<int:trek_id>/assignments", methods=["GET"])
@jwt_required()
@admin_required
def get_trek_assignments(trek_id):

    # Check whether trek exists
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    assignments = StaffAssignment.query.filter_by(trek_id=trek_id).all()

    result = []

    for assignment in assignments:

        staff = User.query.get(assignment.staff_id)

        result.append({
            "id": assignment.id,
            "staff_id": staff.id if staff else None,
            "staff_name": staff.full_name if staff else "Unknown",
            "assigned_on": assignment.assigned_on.isoformat()
        })

    return jsonify(result), 200

# Get assignments for a specific staff member

@admin_bp.route("/staff/<int:staff_id>/assignments", methods=["GET"])
@jwt_required()
@admin_required
def get_staff_assignments(staff_id):

    # Check whether staff exists
    staff = User.query.filter_by(
        id=staff_id,
        role="STAFF"
    ).first()

    if not staff:
        return jsonify({
            "message": "Staff member not found"
        }), 404

    assignments = StaffAssignment.query.filter_by(
        staff_id=staff_id
    ).all()

    result = []

    for assignment in assignments:

        trek = Trek.query.get(assignment.trek_id)

        result.append({
            "id": assignment.id,
            "trek_id": trek.id if trek else None,
            "trek_title": trek.title if trek else "Unknown",
            "assigned_on": assignment.assigned_on.isoformat()
        })

    return jsonify(result), 200


# Delete assignments

@admin_bp.route("/assignments/<int:assignment_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_assignment(assignment_id):

    assignment = StaffAssignment.query.get_or_404(
        assignment_id
    )

    db.session.delete(assignment)

    db.session.commit()

    return jsonify({
        "message": "Assignment removed successfully"
    }), 200

# Booking Routes

@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def get_all_bookings():

    bookings = Booking.query.all()

    result = []

    for booking in bookings:

        user = User.query.get(booking.user_id)
        trek = Trek.query.get(booking.trek_id)

        result.append({
            "booking_id": booking.id,
            "trekker": user.full_name if user else "Unknown",
            "trek": trek.title if trek else "Unknown",
            "number_of_people": booking.number_of_people,
            "status": booking.status,
            "booked_at": booking.booked_at.isoformat()
        })

    return jsonify(result), 200

# Admin Dashboard
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
def admin_dashboard():

    total_users = User.query.count()

    total_staff = User.query.filter_by(
        role="STAFF"
    ).count()

    total_trekkers = User.query.filter_by(
        role="TREKKER"
    ).count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return jsonify({
        "total_users": total_users,
        "total_staff": total_staff,
        "total_trekkers": total_trekkers,
        "total_treks": total_treks,
        "total_bookings": total_bookings
    }), 200