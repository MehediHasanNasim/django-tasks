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
