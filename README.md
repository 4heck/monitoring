# MCW Price-Monitoring
***
1. Clone with SSH: 

    `git clone git@github.com:4heck/monitoring.git`

2. Create and activate virtual environment, download all requirements:
    
    `python3 -m venv venv`
    
    `source venv/bin/activate`

    `cd monitoring/app`
    
    `pip install -r requirements.txt`
    
3. Migrate database:
    
    **Check login/password of your database in `setting.py`**
    
    `python3 manage.py makemigrations`
    
    `python3 manage.py migrate`

4. Create superuser:

    `python3 manage.py createsuperuser`
    
5. Run server:

    `python3 manage.py runserver`
    
6. Open [index page](http://localhost:8000/)


