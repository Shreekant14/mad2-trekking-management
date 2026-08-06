from datetime import datetime

from .extensions import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="UPCOMING")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "location": self.location,
        "difficulty": self.difficulty,
        "duration": self.duration,
        "price": float(self.price),
        "description": self.description,
        "start_date": self.start_date.isoformat(),
        "end_date": self.end_date.isoformat(),
        "total_slots": self.total_slots,
        "available_slots": self.available_slots,
        "status": self.status,
        "created_at": self.created_at.isoformat(),
        "created_by": self.created_by
    }

    def __repr__(self):
        return f"<Trek {self.title}>"


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_people = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="PENDING")

    def __repr__(self):
        return f"<Booking {self.id}>"


class StaffAssignment(db.Model):
    __tablename__ = "staff_assignments"

    id = db.Column(db.Integer, primary_key=True)

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    assigned_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StaffAssignment {self.id}>"