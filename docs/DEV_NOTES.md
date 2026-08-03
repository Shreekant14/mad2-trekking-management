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

---

# Useful Commands

## Create Virtual Environment

python -m venv .venv

---

## Activate

.\.venv\Scripts\Activate.ps1

---

## Install Packages

pip install ...

---

## Save Requirements

pip freeze > requirements.txt

---

## Run Server

python run.py
