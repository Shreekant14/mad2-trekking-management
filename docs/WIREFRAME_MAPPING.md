# Wireframe Mapping

## Overview

This document maps each wireframe screen to the corresponding database tables, backend APIs, and user roles.

---

## 1. Login Page

### Role

- Admin
- Trek Staff
- Trekker

### Database Tables

- User

### APIs

- POST /api/login

### Operations

- Authenticate user
- Redirect based on role

---

## 2. Registration Page

### Role

- Trekker

### Database Tables

- User

### APIs

- POST /api/register

### Operations

- Create new trekker account

---

## 3. Admin Dashboard

### Role

- Admin

### Database Tables

- User
- Trek
- Booking

### APIs

- GET /api/admin/dashboard

### Operations

- View dashboard statistics
- Navigate to management modules

---

## 4. Manage Treks

### Role

- Admin

### Database Tables

- Trek

### APIs

- GET /api/admin/treks
- POST /api/admin/treks
- PUT /api/admin/treks/{id}
- DELETE /api/admin/treks/{id}

### Operations

- Add trek
- Edit trek
- Delete trek
- View all treks

---

## 5. Manage Trek Staff

### Role

- Admin

### Database Tables

- User
- StaffAssignment

### APIs

- GET /api/admin/staff
- POST /api/admin/staff
- PUT /api/admin/staff/{id}
- DELETE /api/admin/staff/{id}
- POST /api/admin/staff/assign

### Operations

- Add staff
- Update staff
- Remove staff
- Assign staff to treks

---

## 6. Manage Users

### Role

- Admin

### Database Tables

- User

### APIs

- GET /api/admin/users
- PUT /api/admin/users/{id}
- DELETE /api/admin/users/{id}

### Operations

- View users
- Update user status
- Remove users

---

## 7. Trek Staff Dashboard

### Role

- Trek Staff

### Database Tables

- StaffAssignment
- Trek

### APIs

- GET /api/staff/dashboard

### Operations

- View assigned treks

---

## 8. Manage Assigned Treks

### Role

- Trek Staff

### Database Tables

- Trek
- Booking
- StaffAssignment

### APIs

- GET /api/staff/treks
- PUT /api/staff/treks/{id}

### Operations

- View assigned trek details
- Update trek information (as permitted)

---

## 9. User Dashboard

### Role

- Trekker

### Database Tables

- Booking
- Trek

### APIs

- GET /api/user/dashboard

### Operations

- View upcoming bookings
- Navigate through the application

---

## 10. Browse Treks

### Role

- Trekker

### Database Tables

- Trek

### APIs

- GET /api/treks

### Operations

- View available treks
- Search treks
- Filter treks

---

## 11. Book Trek

### Role

- Trekker

### Database Tables

- Booking
- Trek

### APIs

- POST /api/bookings

### Operations

- Book a trek
- Update available slots

---

## 12. Trek History

### Role

- Trekker

### Database Tables

- Booking
- Trek

### APIs

- GET /api/user/bookings

### Operations

- View completed bookings
- View cancelled bookings
