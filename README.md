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

4. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the server**
```bash
python manage.py runserver
```

# Project Overview

- CSC540_Backend/: Contains settings, URLs, and configuration files for the Django project.
- zybooks/: Custom Django app for managing textbook, chapter, section, and content models.
- media/: Folder to store uploaded media files.
- db.sqlite3: The SQLite database file for local development.
- requirements.txt: Lists all Python packages required for the project.

# Common Commands
- Run migrations: `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
- Check tables: `python manage.py inspectdb`

# API Documentation
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/17032297-c99120d4-22ab-44ef-bd19-b68e3cd1683f?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17032297-c99120d4-22ab-44ef-bd19-b68e3cd1683f%26entityType%3Dcollection%26workspaceId%3Da77fb22b-002c-4b04-bc9a-122f482bb03a)

# Contributing
1. Fork the repository.
2. Create a new branch: git checkout -b feature/your-feature-name.
3. Make your changes and commit them: git commit -m 'Add feature'.
4. Push to the branch: git push origin feature/your-feature-name.
5. Submit a pull request.

# Licence

### Additions Explained:

- **API Documentation**: Includes instructions for linking Postman API documentation.
  `[<Postman>](https://www.postman.com/oodd33/workspace/rems-workspace/collection/17032297-c99120d4-22ab-44ef-bd19-b68e3cd1683f?action=share&creator=17032297)`. This final version should provide a comprehensive guide for setting up, understanding, and working with the project.
