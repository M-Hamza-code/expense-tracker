# 💰 Expense Tracker API

A RESTful Expense Tracker API built with **FastAPI**, **SQLAlchemy**, **JWT Authentication**, and **Swagger UI**. This project allows users to manage personal expenses, create expense-sharing groups, maintain activity logs, and customize application settings.

---

# 📌 Project Overview

Managing daily expenses manually becomes difficult as the amount of data grows. Users also need secure authentication, proper database storage, expense categorization, group expense sharing, and activity tracking.

This project solves these problems by providing a secure and organized Expense Tracker API with complete CRUD operations and group expense management.

---

# ❗ Problem Statement

The main problems identified were:

* No secure user authentication.
* Expenses were not stored permanently.
* Users could not manage expenses separately.
* No way to calculate totals automatically.
* No expense categorization.
* No monthly filtering.
* No shared/group expense management.
* No activity history.
* No user preference settings.
* APIs were difficult to test without proper documentation.

---

# ✅ Solution

The following solutions were implemented:

* JWT-based authentication system.
* Database integration using SQLAlchemy.
* CRUD operations for expenses.
* User-specific expense management.
* Automatic total calculations.
* Category-wise expense summary.
* Monthly expense filtering.
* Highest & lowest expense analysis.
* Group expense splitting.
* Activity logging.
* User settings management.
* Swagger UI for API testing.

---

# 🛠 Technologies Used

* Python
* FastAPI
* SQLAlchemy ORM
* SQLite Database
* Pydantic
* JWT (python-jose)
* Swagger UI (OpenAPI)

---

# 📂 Project Structure

```
ExpenseTracker/
│
├── database/
├── models/
├── routes/
│   ├── auth.py
│   ├── expenses.py
│   ├── groups.py
│   ├── logs.py
│   └── settings.py
│
├── schemas/
├── services/
├── utils/
├── main.py
└── README.md
```

---

# 🔐 Authentication Module

## Signup

Registers a new user.

**Endpoint**

```
POST /signup
```

Features

* Creates new user
* Prevents duplicate usernames
* Stores user information

---

## Login

Authenticates the user.

**Endpoint**

```
POST /login
```

Features

* Username & password verification
* Generates JWT Token
* Returns Bearer Token for protected APIs

---

# 💸 Expense Management

## Add Expense

```
POST /expenses
```

Features

* Add title
* Amount
* Category
* Stores expense in database
* Records activity log

---

## Get Expenses

```
GET /expenses
```

Returns all expenses of the logged-in user.

---

## Update Expense

```
PUT /expenses/{id}
```

Allows editing:

* Title
* Amount
* Category

---

## Delete Expense

```
DELETE /expenses/{id}
```

Deletes a selected expense and records the action in logs.

---

## Total Expenses

```
GET /expenses/total
```

Calculates total spending automatically.

---

## Clear Expenses

```
DELETE /expenses/clear
```

Deletes all expenses of the logged-in user.

---

## Category Wise Total

```
GET /expenses/category-total
```

Returns total expenses grouped by category.

Example

```
Food : 3000
Travel : 1500
Bills : 5000
```

---

## Monthly Expenses

```
GET /expenses/monthly
```

Filters expenses by month and year.

---

## Monthly Total

```
GET /expenses/monthly-total
```

Calculates total spending of a selected month.

---

## Highest Expense

```
GET /expenses/highest
```

Returns the most expensive transaction.

---

## Lowest Expense

```
GET /expenses/lowest
```

Returns the smallest transaction.

---

# 👥 Group Expense Module

Users can share expenses with multiple members similar to Splitwise.

---

## Create Group

```
POST /groups
```

Creates a new expense-sharing group.

---

## Add Member

```
POST /groups/{group_id}/add
```

Features

* Only owner can add members
* Validates registered users
* Prevents duplicate members

---

## View Groups

```
GET /groups
```

Returns all groups created by the logged-in user.

---

## View Single Group

```
GET /groups/{group_id}
```

Displays

* Group information
* Owner
* Members

---

## Add Group Expense

```
POST /groups/{group_id}/expense
```

Features

* Records group expense
* Automatically splits amount equally
* Saves individual shares

---

## View Group Expenses

```
GET /groups/{group_id}/expenses
```

Shows all expenses inside a group.

---

## Group Balance

```
GET /groups/{group_id}/balance
```

Calculates:

* Paid Amount
* Share Amount
* Remaining Balance

---

## Delete Member

```
DELETE /groups/{group_id}/member/{username}
```

Owner can remove any member.

---

## Delete Expense

```
DELETE /groups/{group_id}/expense/{expense_id}
```

Owner can delete group expenses.

---

## Delete Group

```
DELETE /groups/{group_id}
```

Deletes

* Group
* Members
* Expenses

---

# 📋 Activity Logs

Every important action is stored.

Examples

* CREATE_GROUP
* ADD_MEMBER
* ADD_EXPENSE
* UPDATE_EXPENSE
* DELETE_EXPENSE
* DELETE_GROUP

Endpoint

```
GET /logs
```

Users can also filter logs by group.

---

# ⚙ User Settings

Users can save personal preferences.

Endpoint

```
POST /settings
```

Stores

* Currency
* Theme

Retrieve settings

```
GET /settings
```

---

# 🔒 Security

Authentication is implemented using JWT.

Protected APIs require:

```
Authorization

Bearer <token>
```

Every expense is linked to its owner, ensuring users cannot access another user's data.

---

# 🗄 Database

The project uses SQLAlchemy ORM.

Main tables include:

* Users
* Expenses
* Groups
* Group Members
* Group Expenses
* Expense Split
* Activity Logs
* User Settings

---

# 📖 API Documentation

FastAPI automatically generates Swagger documentation.

Run the project and open:

```
http://127.0.0.1:8000/docs
```

Interactive API testing is available through Swagger UI.

---

# 🚀 Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Start server

```bash
uvicorn main:app --reload
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

---

# ✅ Features Summary

* JWT Authentication
* FastAPI REST APIs
* SQLAlchemy Database
* Expense CRUD Operations
* Category Wise Summary
* Monthly Reports
* Highest & Lowest Expense
* Group Expense Sharing
* Automatic Expense Split
* Activity Logging
* User Settings
* Swagger Documentation
* Secure User-Based Access

---

# 👨‍💻 Conclusion

This Expense Tracker API provides a complete backend solution for personal and shared expense management. By combining FastAPI, SQLAlchemy, JWT authentication, and Swagger documentation, the application offers secure authentication, organized data management, automatic calculations, activity tracking, and group expense sharing in a scalable and maintainable architecture.
