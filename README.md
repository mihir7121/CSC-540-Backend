# CSC-540-Backend

A Django-based backend for the CSC-540 project, providing REST APIs and media handling. This project includes a custom application, `zybooks`, and uses an SQLite database.

We will work under the 'zybooks' app throughout the project while using 'CSC-540-Backend' folder for project configurations.


## Requirements

- Python 3.x
- Django
- Any additional dependencies listed in `requirements.txt`

## Setup Instructions

1. **Clone the repository:**
```bash
   git clone <repository-url>
   cd CSC-540-Backend
```
2. **Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Add .env file in CSC540_Backend folder**
```bash
SECRET_KEY = "SECRETKEY"
DEBUG=True
```

5. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Run the server**
```bash
python manage.py runserver
```
The development server should now be accessible at `http://127.0.0.1:8000`.

# Project Overview

- CSC540_Backend/: Contains settings, URLs, and configuration files for the Django project.
- zybooks/: Custom Django app for managing textbook, chapter, section, and content models.
- media/: Folder to store uploaded media files.
- db.sqlite3: The SQLite database file for local development.
- requirements.txt: Lists all Python packages required for the project.


The E-Learning Application is a Django-based platform designed to manage digital textbooks, courses, and student engagement through activities. It supports a collection of e-textbooks, each with chapters, sections, and content blocks (text or images) organized in a hierarchical structure. Admins can create and manage textbooks, while faculty members can create course instances based on these textbooks. Courses are either "active," which allow student enrollment and can include teaching assistants (TAs), or "evaluation," which do not have enrollment, TAs, or a unique access code. Faculty and TAs can also customize course content by hiding sections, adding new content, and renumbering sections to ensure coherent flow for students. Customizations, however, respect hierarchical restrictions: faculty cannot alter the base textbook content added by admins, and TAs cannot modify faculty entries.

The application supports four primary user roles: admin, faculty, student, and TA. Admins manage textbooks and course creation, faculty handle course enrollments and content modifications, TAs assist faculty in content management, and students access course content and participate in interactive activities. Students can view content sequentially, attempt quizzes associated with sections, and earn participation points based on their performance. The system maintains a flexible content numbering scheme to accommodate dynamic changes. Faculty and students can also view notification messages stored in a database, and students can monitor their participation points against the total possible score for each course. This structure ensures an organized and customizable e-learning experience, promoting user engagement through an interactive textbook model.


# Common Commands
- Run migrations: `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Make migrations: `python manage.py makemigrations`
- Check tables: `python manage.py inspectdb`

# API Documentation
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/17032297-c99120d4-22ab-44ef-bd19-b68e3cd1683f?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17032297-c99120d4-22ab-44ef-bd19-b68e3cd1683f%26entityType%3Dcollection%26workspaceId%3Da77fb22b-002c-4b04-bc9a-122f482bb03a)

# Contributing
1. Fork the repository.
2. Create a new branch: git checkout -b feature/your-feature-name.
3. Make your changes and commit them: git commit -m 'Add feature'.
4. Push to the branch: git push origin feature/your-feature-name.
5. Submit a pull request.
