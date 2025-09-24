
# Student Assignment Tracker (Django)
A simple Django web app that allows students to register/login and upload assignments. Admin/teachers can view all submissions and mark them as reviewed.

## Features
- User registration and login (Django auth)
- CRUD for assignments (title, description, file upload)
- Student sees only their submissions
- Admin sees all, can mark as reviewed

## Requirements
- Python 3.10+
- pip

## Setup (Windows/Mac/Linux)
```bash
# 1) Extract the zip
cd student_assignment_tracker

# 2)  Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Create DB & superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5) Run
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Default URLs
- `/` Home → redirects to assignments
- `/assignments/` list + create/edit/delete
- `/accounts/login/` login
- `/accounts/logout/` logout
- `/register/` user registration
- `/admin/` admin site

## Notes
- Uploaded files are saved under `media/assignments/`
- Create 'media/'
- To change DEBUG or SECRET_KEY, edit `student_assignment_tracker/settings.py`
- For production, configure STATIC/MEDIA in a proper web server.

- see password.txt for test users
