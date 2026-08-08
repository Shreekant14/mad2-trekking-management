# Project Journal

## Day 1

### Completed

- Created GitHub repository
- Read project requirements
- Reviewed wireframes
- Planned development workflow
- Created project documentation:
  - README.md
  - DATABASE_DESIGN.md
  - WIREFRAME_MAPPING.md

### Next

- Set up backend development environment

---

## Milestone 0 - Backend Setup

### Completed

- Created Python virtual environment
- Installed required Python packages
- Generated requirements.txt
- Created backend folder structure
- Organized route modules using Flask Blueprints
- Created initial Flask application configuration

### Next

- Run Flask application successfully

## Milestone 0 - Initial Commit

### Completed

- Initialized Git repository
- Added project documentation
- Set up Flask backend
- Created application structure
- Pushed initial project to GitHub

### Git Commit

setup: initialize project structure and Flask backend

## Milestone 1 - User Model

### Completed

- Created User model using SQLAlchemy
- Initialized SQLite database
- Generated users table
- Verified Flask application creates database successfully

### Git Commit

feat(models): create User model and initialize database

### Next

Implement Trek model

## Milestone 1 - Database Layer

### Completed

- Created User model
- Created Trek model
- Created Booking model
- Created StaffAssignment model
- Configured Flask-Migrate
- Generated initial database migration
- Resolved migration detection issue

### Git Commit

feat(database): add models and configure Flask-Migrate

### Next

Authentication Module

# Project Journal

---

## Date: 06 August 2026

## Milestone 2 - Authentication Module

### Completed

- Implemented password hashing using Flask-Bcrypt
- Developed user registration API
- Developed user login API
- Implemented JWT authentication
- Created protected API endpoint
- Successfully tested all authentication APIs

### APIs Completed

POST /api/auth/register
POST /api/auth/login
GET /api/auth/profile

### Git Commit

feat(auth): implement JWT authentication

### Next

Admin Module - Trek Management

## Milestone 3 - Admin Trek Management

### Completed

- Implemented role-based authorization using custom decorators.
- Developed complete Trek CRUD APIs.
- Added Trek model serialization using `to_dict()`.
- Protected all admin endpoints using JWT and RBAC.
- Successfully tested all CRUD operations.
- Verified Trekker users cannot access Admin APIs.

### APIs Completed

POST /api/admin/treks
GET /api/admin/treks
GET /api/admin/treks/<id>
PUT /api/admin/treks/<id>
DELETE /api/admin/treks/<id>

### Issues Resolved

- Flask-Migrate not detecting models.
- Missing `to_dict()` method in Trek model.

### Git Commit

feat(admin): implement trek management CRUD with RBAC

# Milestone 4

# Milestone 5 – Booking Module & Backend Completion

## Completed

- Implemented Trekker APIs.
- Trek browsing.
- Trek booking.
- My bookings.
- Booking cancellation.
- Staff assignment APIs.
- Staff management APIs.
- Admin booking management.
- Dashboard API planning.

## Testing

Successfully tested:

- Trek CRUD
- User CRUD
- Staff CRUD
- Staff Assignment
- Trek Browsing
- Trek Booking
- Booking Cancellation
- JWT Authentication
- RBAC Authorization

## Challenges Faced

- Missing Blueprint registration.
- Incorrect Flask route parameter syntax.
- Missing `to_dict()` method.
- Flask-Migrate model detection issue.
- Duplicate staff assignment handling.
- Booking slot synchronization.

## Learning

- Flask Blueprints
- JWT Authentication
- Role-Based Authorization
- SQLAlchemy Relationships
- REST API Design

### Bug Fix

While testing Staff APIs, login failed with an `Invalid salt` error.

Investigation showed that one test staff account had been created using an older password hashing method before the project standardized on Flask-Bcrypt.

The old test account was removed and recreated through the Staff Creation API. After recreating the account, authentication worked correctly.

# Milestone 6 – Backend Feature Completion

## Goal

Complete all remaining backend APIs for the Trekking Management System.

---

## Work Completed

### Admin Module

- Trek CRUD
- User Management
- Staff Management
- Staff Assignment
- Booking Management
- Dashboard API

### Staff Module

- My Treks
- Participants List
- Dashboard API

### Trekker Module

- Browse Treks
- Book Trek
- View My Bookings
- Cancel Booking
- Dashboard API

---

## Testing Performed

Successfully tested:

- User Registration
- User Login
- JWT Authentication
- Role-Based Authorization
- Trek CRUD
- User CRUD
- Staff CRUD
- Staff Assignment
- Trek Booking
- Booking Cancellation
- Trek Browsing
- Staff APIs
- Dashboard APIs

---

## Issues Faced

1. Blueprint registration missing.

Result:

404 errors.

Resolved by registering all Blueprints inside `create_app()`.

---

2. Incorrect Flask route parameter syntax.

Used:

```
/staff/int:staff_id
```

Corrected to:

```
/staff/<int:staff_id>
```

---

3. Flask-Migrate schema detection issue.

Resolved by importing models inside `create_app()` before migrations.

---

4. Password hashing inconsistency.

One test user used an old hashing method.

Resolved by deleting the user and recreating it using Flask-Bcrypt.

---

## What I Learned

- Flask Blueprints
- JWT Authentication
- Role-Based Access Control
- SQLAlchemy Relationships
- REST API Design
- Database Migrations
- Debugging Flask Applications
- API Testing
