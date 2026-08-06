# Development Notes

## Backend

### Why did we use Blueprints?

Instead of keeping every route in one routes.py file, we created separate modules:

- auth.py → Login & Register
- admin.py → Admin APIs
- staff.py → Trek Staff APIs
- trekker.py → Trekker APIs

Benefits

- Keeps authentication, admin, staff and trekker routes independent.
- Prevents one large routes.py file.
- Makes debugging easier.
- Allows each module to grow independently.

---

## Flask-Migrate

Purpose

Flask-Migrate manages database schema changes using migrations.

Advantages

- Keeps database version history.
- Updates existing databases safely.
- Avoids deleting and recreating the database.
- Suitable for production applications.

---

## SQLAlchemy

### SQLAlchemy Model

A model is a Python class that represents a database table.

Each object of the class represents one row in that table.

Example:

User Model

↓

users table

↓

One User object = One database record.

## Why use SQLAlchemy instead of raw SQL?

SQLAlchemy is an ORM (Object Relational Mapper).

Benefits:

- Write Python instead of SQL.
- Database-independent.
- Easier relationships.
- Cleaner code.
- Less SQL injection risk.

## SQLAlchemy Column Options

primary_key=True

- Makes the column the primary key.

unique=True

- Prevents duplicate values.

nullable=False

- Makes the field mandatory.

default=value

- Assigns a default value if none is provided.

---

app = create_app()

Creates the Flask application.

with app.app_context():

This gives Flask access to its configuration.

Without this you'll get an error like:

Working outside of application context.

You'll probably see this error at least once in your Flask journey 😄.

db.create_all()

This is the magic.

It tells SQLAlchemy:

"Look at every model that inherits from db.Model and create the corresponding tables if they don't already exist."

Since we currently have only one model:

class User(db.Model):

SQLAlchemy creates only one table:

users

## db.create_all()

Purpose

Creates database tables from SQLAlchemy models.

How it works

1. Reads every class that inherits from db.Model.
2. Generates SQL CREATE TABLE statements.
3. Creates tables that do not already exist.

Note

db.create_all() only creates missing tables.
It does not update existing tables.

---

## Foreign Key

A Foreign Key is a column that references the primary key of another table.

Example:

Booking.user_id → User.id

Purpose:

- Maintains referential integrity.
- Prevents invalid references.
- Connects related tables.

## Password Hashing

Passwords should never be stored in plain text.

Flask-Bcrypt converts passwords into a secure hash before storing them.

During login, the entered password is hashed and compared with the stored hash.

Methods used:

- set_password()
- check_password()

## Registration API Flow

1. Receive JSON request.
2. Validate required fields.
3. Check if email already exists.
4. Hash the password.
5. Save the user.
6. Return success response.

## JWT Authentication Flow

1. User submits email and password.
2. Server verifies credentials.
3. Server generates a JWT access token.
4. Client stores the token.
5. Client sends the token in the Authorization header.
6. Protected APIs validate the token before processing the request.

## Role-Based Access Control (RBAC)

Authentication verifies who the user is.

Authorization verifies what the user is allowed to do.

JWT identifies the user.

Custom decorators (such as @admin_required) enforce role-based authorization.

## CRUD Operations

CRUD stands for:

- Create → POST
- Read → GET
- Update → PUT
- Delete → DELETE

These four operations form the foundation of RESTful APIs.

## Why use to_dict()?

SQLAlchemy model objects cannot be returned directly as JSON.

The `to_dict()` method converts a model instance into a dictionary, making it easy to return JSON responses and avoiding repetitive code in API routes.

## Why use a custom decorator for RBAC?

Instead of checking the user's role inside every API, we created a reusable `@admin_required` decorator.

Benefits:

- Avoids duplicate code.
- Keeps routes clean.
- Makes authorization reusable.
- Easier to maintain.

---

# Viva Questions

Q. Why did you use Flask instead of Django?

Answer:

Flask is a lightweight micro-framework.

It provides only the essential components required to build a web application, allowing developers to choose additional libraries as needed.

Since the MAD 2 project requires REST APIs and custom application logic rather than Django's built-in features like the admin panel or ORM conventions, Flask offers greater flexibility and keeps the application lightweight.

---

Q. Why Blueprint?

Answer

Blueprint is a Flask feature used to organize related routes into separate modules.

Instead of writing all routes in a single file, Blueprints allow us to divide the application into logical sections such as authentication, admin, staff, and trekker.

This improves readability, maintainability, and scalability.
...

Q. Difference between JWT and Session?

Answer:
Session authentication stores user information on the server.

JWT stores user identity inside a signed token that is sent with each request.

Sessions are stateful.

JWT is stateless.

For REST APIs, JWT is preferred because the frontend and backend communicate independently.

Q. What is ORM?

Answer:

ORM (Object Relational Mapping) is a technique that maps database tables to Python classes. Instead of writing SQL queries directly, developers interact with Python objects, and the ORM automatically generates the required SQL.

Q1. Why did we create a User model?

Expected answer:

The User model stores information about all users of the application. Instead of creating separate tables for Admin, Trek Staff, and Trekker, we use a single table with a role field. This reduces duplication and simplifies authentication and authorization.

Q. Why is email marked as unique=True?

Expected answer:

Every user must have a unique email address because email is used for login. The database enforces uniqueness to prevent duplicate accounts.

Q3. Why are we storing password_hash instead of password?

Expected answer:

Passwords should never be stored in plain text. They are hashed before being stored so that even if the database is compromised, the original passwords cannot be easily recovered.

Q4. Why didn't we use three tables (Admin, Staff, Trekker)?

Expected answer:

All three roles share common information like name, email, phone, and password. Using one table with a role column avoids duplicate data and makes authentication simpler.

Q5. Why do we have created_at?

Expected answer:

It records when the account was created. This can be useful for sorting users, generating reports, auditing, and debugging.

Q. What does db.create_all() do?

Answer:

db.create_all() creates database tables from SQLAlchemy models. It checks all models that inherit from db.Model and creates only the tables that do not already exist. It does not modify existing tables.

Q. What is a Primary Key?

Answer:

A Primary Key uniquely identifies each record in a table. It cannot contain duplicate or NULL values.

Q. What is a Foreign Key?

Answer:

A Foreign Key is a column that references the Primary Key of another table. It establishes a relationship between two tables and maintains data integrity.

Q. Why use Flask-Migrate instead of db.create_all()?

Answer:

db.create_all() only creates missing tables and cannot modify existing tables. Flask-Migrate tracks schema changes and generates migration scripts, allowing databases to evolve safely without losing data.

Q. Why didn't Flask-Migrate detect your tables initially?

Answer

Flask-Migrate generates migrations using SQLAlchemy's metadata.

Initially, the models were not imported into the Flask application, so the metadata was empty and Alembic could not detect any tables.

Importing the models inside `create_app()` solved the issue.

Q. Why do we check for duplicate emails in both the code and the database?

Answer:

The application checks first to provide a user-friendly error message. The database also enforces uniqueness using unique=True, ensuring data integrity even if the application logic is bypassed.

Q. Why do APIs return JSON instead of HTML?

Answer:

The frontend (Vue.js) communicates with the backend using HTTP APIs. JSON is lightweight, language-independent, and easy for frontend applications to parse.

Q. What is JWT?

Answer:

JWT (JSON Web Token) is a secure, digitally signed token used for authentication. After a successful login, the server generates a token that the client sends with future requests to access protected resources.

Q. Why don't users log in on every request?

Answer:

After logging in once, the client stores the JWT token and includes it in the Authorization: Bearer <token> header for subsequent requests. The server validates the token instead of asking for credentials again.

Q. Why did you choose JWT instead of Session Authentication?

Answer

The frontend (Vue.js) and backend (Flask) are separate applications that communicate using REST APIs.

JWT is stateless and is well suited for REST APIs because the server does not need to store session information.

The client sends the token with each request, and the server verifies it before granting access.

Q. What is the difference between Authentication and Authorization?

Answer:

Authentication verifies the identity of a user (Login using email and password).
Authorization determines what the authenticated user is allowed to access (Admin, Trek Staff, Trekker).

JWT provides authentication, while our custom decorators implement authorization.

Q. Why do we use different HTTP methods?

POST → Create a resource

GET → Retrieve data

PUT → Update an existing resource

DELETE → Remove a resource

Using standard HTTP methods makes APIs predictable and RESTful.

## Password Hashing

Passwords should never be stored in plain text.

Flask-Bcrypt converts passwords into a secure hash before storing them.

During login, the entered password is hashed and compared with the stored hash.

Methods used:

- set_password()
- check_password()

# Mistakes Made

1.

Forgot to activate virtual environment.

Solution

Always activate .venv before running.

---

2.

Initially planned one routes.py

Changed to Blueprints.

Reason

Cleaner architecture.

3. Flask-Migrate detected removed table / No changes in schema detected

### Problem

Initially, Flask-Migrate generated an incorrect migration:

```
Detected removed table 'users'
```

After deleting the database and migrations folder, it generated:

```
No changes in schema detected.
```

### Cause

The SQLAlchemy models were never imported inside the Flask application.

Flask-Migrate only detects models that are imported and registered with SQLAlchemy.

Since `models.py` was not imported, Alembic considered the metadata empty.

### Solution

Added the following line inside `create_app()` after initializing extensions:

```python
from . import models
```

Then:

1. Deleted the `migrations/` folder.
2. Deleted `instance/trekking.db`.
3. Ran:

```bash
flask db init
flask db migrate -m "Initial database schema"
flask db upgrade
```

Result:

```
Detected added table 'users'
Detected added table 'treks'
Detected added table 'bookings'
Detected added table 'staff_assignments'
```

### Learning

Flask-Migrate only creates migrations for models that have been imported.

Always ensure models are imported before generating migrations.

---

# Useful Commands

## Create Virtual Environment

python -m venv .venv

---

## Install Packages

pip install ...

---

## Save Requirements

pip freeze > requirements.txt

---

## Activate

.\.venv\Scripts\Activate.ps1

---

## Run Server

python run.py
