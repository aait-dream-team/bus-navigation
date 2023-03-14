**Bus Navigation Backend**

The repo contains the main business logic backend of the bus navigation project

**Steps to run**

1. Clone the repo
2. Create a separate virtual environment
    
    - `python3 -m venv env`
3. Activate your virtual environment
    
    - `source env/bin/activate`
4. Install requirements
    
    - `pip install -r requirements.txt`
5. Install postgres and create a database called bus_navigation
6. Edit the databases variable in `bus_navigation_backend/bus_navigation_backend/settings.py` to your database configuration
7. Make and run migrations

    - `python manage.py makemigrations`
    - `python manage.py migrate`
8. Run the server
    - `python wait_for_postgres.py && ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000`