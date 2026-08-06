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
