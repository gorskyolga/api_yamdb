# api_yamdb
## Description
API for **Yamdb project**

Yamdb project is a platform for reviews of various works of art.
It is possible to set a rating and add comments to reviews of other users.
## Technologies
Python 3.9, Django 3.2, Django Rest Framework 3.12, SQLite
## Running a project in dev-mode
1. Clone the repository and change to it on the command line
2. Install and activate the virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
_OR for Windows_
```
python -m venv venv
source venv/Scripts/activate
```
3. Upgrade pip if necessary and install requirements from **requirements.txt**
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
_OR for Windows_
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Change the current directory to **api_yamdb** and run migrations
```
cd api_yamdb
python3 manage.py migrate
```
_OR for Windows_
```
cd api_yamdb
python manage.py migrate
```
5. If necessary, import initial data from the csv files (api_yamdb/static/data) into the Data Base
```
python3 manage.py import_initial_data
```
_OR for Windows_
```
python manage.py import_initial_data
```
6. Run the project
```
python3 manage.py runserver
```
_OR for Windows_
```
python manage.py runserver
```
### API request examples
See the documentation for the examples: http://127.0.0.1:8000/redoc
### Authors
- AndreiFilatov, gorskyolga, posredn1k
- yandex-praktikum (Yandex Praktikum)
