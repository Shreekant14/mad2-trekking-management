# Database Design

## Overview

The Trekking Management Application uses a relational database to manage users, treks, bookings, and staff assignments. The database is designed to maintain data consistency while supporting all the required features of the application.

---

## Entities

### 1. User

Stores information about all users of the system.

| Field         | Type         | Description                  |
| ------------- | ------------ | ---------------------------- |
| id            | Integer (PK) | Unique user ID               |
| full_name     | String       | User's full name             |
| email         | String       | User email (unique)          |
| password_hash | String       | Encrypted password           |
| phone         | String       | Contact number               |
| role          | Enum         | ADMIN / TREK_STAFF / TREKKER |
| is_active     | Boolean      | Account status               |
| created_at    | DateTime     | Account creation date        |

---

### 2. Trek

Stores details of trekking events.

| Field           | Type         | Description                                |
| --------------- | ------------ | ------------------------------------------ |
| id              | Integer (PK) | Unique trek ID                             |
| title           | String       | Trek name                                  |
| location        | String       | Trek location                              |
| difficulty      | String       | EASY / MODERATE / HARD                     |
| duration        | Integer      | Duration in days                           |
| price           | Decimal      | Trek fee                                   |
| description     | Text         | Trek description                           |
| start_date      | Date         | Trek start date                            |
| end_date        | Date         | Trek end date                              |
| total_slots     | Integer      | Maximum participants                       |
| available_slots | Integer      | Remaining slots                            |
| status          | String       | UPCOMING / ONGOING / COMPLETED / CANCELLED |
| created_by      | Integer (FK) | Admin who created the trek                 |

---

### 3. Booking

Stores trek booking details.

| Field            | Type         | Description                                 |
| ---------------- | ------------ | ------------------------------------------- |
| id               | Integer (PK) | Booking ID                                  |
| user_id          | Integer (FK) | User who booked                             |
| trek_id          | Integer (FK) | Booked trek                                 |
| booking_date     | Date         | Booking date                                |
| number_of_people | Integer      | Number of participants                      |
| status           | String       | PENDING / CONFIRMED / CANCELLED / COMPLETED |

---

### 4. Staff Assignment

Stores staff assigned to treks.

| Field       | Type         | Description           |
| ----------- | ------------ | --------------------- |
| id          | Integer (PK) | Assignment ID         |
| staff_id    | Integer (FK) | Assigned staff member |
| trek_id     | Integer (FK) | Assigned trek         |
| assigned_on | Date         | Assignment date       |

---

## Relationships

User (1) -------- (M) Booking

Trek (1) -------- (M) Booking

User (TREK_STAFF) (1) -------- (M) StaffAssignment

Trek (1) -------- (M) StaffAssignment

---

## Database Summary

The database consists of four main tables:

- User
- Trek
- Booking
- StaffAssignment

These tables provide the foundation for:

- Authentication
- Role-based access control
- Trek management
- Trek booking
- Staff assignment
- User management

Additional tables can be added later if new features are introduced.
