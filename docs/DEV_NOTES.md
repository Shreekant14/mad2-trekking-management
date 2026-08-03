# Development Notes

## Why did we use Blueprints?

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
