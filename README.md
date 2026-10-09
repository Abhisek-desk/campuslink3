# CampusLink

Campus-to-corporate placement platform (prototype). Django REST backend + React/Vite frontend.

## Roles
Student, Recruiter, Placement Officer, Mentor. Students are added to the roster by the officer and then activate their account; recruiters register and wait for officer approval.

## Run the backend
Requires Python 3.11+ and MySQL (database `campuslink`, user `campus` / `campus123`, see `backend/config/settings.py`).

```bash
cd backend
python -m venv env && source env/bin/activate      # Windows: env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                # optional, only for real emails
python manage.py migrate
python manage.py createsuperuser                    # superusers are placement officers
python manage.py runserver
```

## Run the frontend
```bash
cd frontend
npm install
npm run dev          # http://localhost:5173  (proxies /api to http://127.0.0.1:8000)
```

## Structure
- `backend/` Django apps: accounts, students, jobs, drives, offers, analytics, engine (NLP, scoring, matching, risk)
- `frontend/src/pages` one page per screen, grouped by role; `components/Layout.jsx` is the shell (navbar, sidebar, dark mode)
