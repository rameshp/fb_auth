# FB Authentication App

### Steps

- pip install -r requirements.txt
- Get client id and client secret code from facebook and add it in local file. Point same file path in fb_auth/settings.py to FB_CONFIG:secret_file_path settings
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver