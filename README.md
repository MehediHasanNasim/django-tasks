# Multi-Tenant Invitation System (Task 1)

This project implements a simple **multi-tenant invitation system** using Django and Django REST Framework.  
Users can be invited to a tenant via email, accept/cancel the invitation, and invitations automatically expire after 7 days.

---

## Features
- Create an invitation (status = `pending`, auto-generate secure token).
- Accept invitation via token and set password (creates a user in the tenant).
- Cancel invitation (only if still pending).
- Invitations expire automatically after 7 days.
- Bonus: Store metadata like IP address or custom note with invitation.

---

## Tech Stack
- **Django** (Backend framework)
- **Django REST Framework** (API support)
- **SQLite** (default DB, can be changed via `.env`)
- **python-decouple** (for environment variables)
- **Celery / Custom Management Command** (to handle expired invitations)

---

## Installation & Setup

1. Clone repository:
   ```bash
   git clone https://github.com/your-username/multi-tenant-invitation.git
   cd multi-tenant-invitation

Create virtual environment & install dependencies:

   ```bash
   python -m venv venv 
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   Configure .env file:

   env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-password
   EMAIL_USE_TLS=True
   ```

Run migrations:
```bash
python manage.py migrate
```
Start server:
```bash
python manage.py runserver
```
API Endpoints
Create Invitation
```bash
POST /api/invitations/

json

{
  "name": "John Doe",
  "email": "john@example.com",
  "tenant": 1,
  "ip_address": "127.0.0.1",
  "note": "Team member"
}

```
Accept Invitation
```bash
POST /api/invitations/accept/

json

{
  "token": "generated_token_here",
  "password": "newpassword123"
}
```

Cancel Invitation
```bash
POST /api/invitations/{id}/cancel/

Expiration Handling
By default, invitations expire 7 days after creation.
```

Expired invitations are marked via:
```bash
python manage.py mark_expired_invitations
```



# Task 2: Permission-Aware Endpoint Decorator

## Goal
Enforce **permission checks** using a **product-feature-role mapping** system.

---

## Features
- Define **Products**, **Features**, **Roles**, and **RoleFeaturePermissions**.
- Apply the `@check_permission` decorator on any view to enforce access control.
- Supports multi-tenant system via `Tenant` and `CustomUser`.
- Returns `401` if unauthenticated, `403` if permission denied.

---

## Models
- **Product** → Represents a product (e.g., `"abc"`).
- **Feature** → A feature within a product (e.g., `"dashboard"`).
- **Role** → Assigned per tenant (e.g., `"Admin"`, `"Viewer"`).
- **RoleFeaturePermission** → Defines which roles can perform which actions (`read`, `write`, `delete`) on features.

---



# Task 3: Centralized Logging with Django Microservices

This project demonstrates a **centralized logging system** for a distributed Django microservices architecture.  
It includes two services (**auth-service** and **tenant-service**) that forward structured JSON logs to **Grafana Loki** using **Promtail**, with visualization in **Grafana**.

---

## 🚀 Features
- **Two Django microservices**:
  - `auth-service` → authentication-related APIs
  - `tenant-service` → tenant management APIs
- **Structured JSON Logging** using [`python-json-logger`](https://github.com/madzak/python-json-logger)
- **Logging Fields**:
  - Timestamp
  - Service Name
  - Request/Trace ID (distributed tracing)
  - Log Level
  - Message
  - (Optional) User ID, Tenant ID
- **Trace ID Propagation** across services using custom middleware
- **Central Logging Backend**:
  - Logs shipped to **Grafana Loki** via **Promtail**
  - Logs visualized in **Grafana dashboards**


## ⚡ How to Run

### 1. Start Monitoring Stack
```bash
docker-compose up -d
```

### 2. Run Django Services
```bash
cd auth-service
python manage.py runserver 0.0.0.0:8000

cd tenant-service
python manage.py runserver 0.0.0.0:8001

```


### 3. Test Logging
```bash
http://localhost:8001/api/tenant/log/?tenant_id=123&user_id=mehedi

http://localhost:8000/api/auth/log/?user_id=nasim
```


# Task 4: Circuit Breaker Demo - Django Middleware

## Overview

This project demonstrates a **Circuit Breaker pattern** implemented as Django middleware.  
It prevents repeated calls to failing external services by temporarily blocking requests when failures exceed a threshold.

---


---

## Features

- **Circuit Breaker Middleware**
  - Monitors failed responses from selected domains (e.g., Auth, Billing API).
  - Opens circuit if failures exceed threshold (3 failures in 1 minute).
  - Blocks outbound requests for 2 minutes when circuit is open.
  - Tracks failure counts using Django cache (memory or Redis).

- **Logging**
  - Logs circuit state changes, failures, and blocked requests.

- **Demo Endpoints**
  - `/api/auth/` → Simulates call to monitored Auth service.
  - `/api/billing/` → Simulates call to monitored Billing service.

---

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd circuit_breaker_demo

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt
python manage.py runserver
```

Configuration:
```bash
FAILURE_THRESHOLD = 3           # Failures to trigger circuit
FAILURE_WINDOW = 60             # Seconds to count failures
BLOCK_TIME = 120                # Seconds circuit remains open
MONITORED_DOMAINS = ['auth-service.com', 'billing-service.com']
```






