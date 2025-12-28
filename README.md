# Secure Multi-Tenant Task Management System (Django + DRF)

## Features

- Multi-tenant architecture (company-based isolation)
- Role-based access control (Manager / Reportee)
- Secure authentication using Django sessions
- Strict ownership & permission enforcement
- Soft delete for tasks
- Pagination for task listing
- Configurable API rate limiting
- Clean, scalable project structure

## Local Setup (macOS)

This project was developed and tested on **macOS (MacBook)** using the following environment:


## Tech Stack

- **Python** 3.10+
- **Django**
- **Django REST Framework**
- **SQLite** (local development)
- **Session-based authentication**
- **Custom permission system**


### Clone the Repository
git clone <repository-url>

### Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

### Install Dependencies
pip install -r requirements.txt

### Database Setup

Run migrations:

```
python manage.py makemigrations
python manage.py migrate
```

Run the Server
```
python manage.py runserver
```


Server will start at:

http://127.0.0.1:8000/


---

# Role-Based Permission Design

## Permissions are defined centrally using a capability-based model:

ROLE_PERMISSIONS = {
    "MANAGER": {
        "task:create",
        "task:assign",
        "task:update:any",
        "task:delete",
        "reportee:create",
        "task:view",
    },
    "REPORTEE": {
        "task:view",
        "task:update:self",
    },
}

Views declare required permissions explicitly:

```
permission_classes = [HasPermission]
required_permission = "task:assign"
```

This design allows:

Easy addition of new roles

Fine-grained access control

Clean separation of business rules


# Multi-Tenant Isolation Strategy

- Every User belongs to exactly one Company

- Every Task is scoped to a Company

- Managers can access only their own tasks

- No cross-company or cross-manager data leakage

- This isolation is enforced at the ORM query level, not just in business logic.




## Soft Delete Strategy

- Tasks are never hard-deleted.

```
is_deleted = models.BooleanField(default=False)
```


All task queries include:

```is_deleted=False```


# Benefits:

- Prevents accidental data loss

- Enables future recovery / auditing

- Safer for production systems




# Pagination

- Task listing uses manual pagination for clarity and control.

Configurable in:

# core/config.py
TASK_LIST_PAGINATION_SIZE = 10


# Pagination rules:

- Page validation enforced

- Returns total count and max page

- Ordered by most recent first

# Rate Limiting

- API abuse protection is implemented using DRF throttling.

##Examples:

- Signup: limited per IP

-- Task creation: limited per user

-- Task listing: limited per user

-- Throttle classes are applied per-view and configurable centrally.

---




# Roles & Permissions
## Manager

- Can sign up and log in

- Can create reportees

- Can create tasks

- Can assign tasks to own reportees

- Can update task status to any value

- Can soft delete tasks

- Can view only tasks created by themselves

## Reportee

- Can log in using manager-created credentials

- Can view only tasks assigned to them

- Can update task status only to COMPLETED

---








## Possible Improvements

- Add proper application logging for important actions and errors.

- Enforce password complexity rules during signup.

- Add account lockout after multiple failed login attempts.

- Improve request and response validation error logging.

- Add task priority support (`LOW`, `MEDIUM`, `HIGH`).

- Add an API to list all reportees under a manager.

- Add task categories for better task organization.

- Add database indexing on task-related columns to improve query performance.

- Add filtering and searching capabilities on tasks.

- Use Redis to improve performance for filtering, searching, and rate limiting.
