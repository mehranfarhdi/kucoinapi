pip install -r requirements.txt
celery -A kucoinapi worker -l info -P gevent
celery -A kucoinapi beat -l info
python manage.py runserver 0.0.0.0:8000
