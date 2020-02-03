cd ..
cd ..
. venv/bin/activate
python manage.py init_conf core
# python manage.py runserver 00.0.0.0:8024
nohup python manage.py runserver 00.0.0.0:8024 &