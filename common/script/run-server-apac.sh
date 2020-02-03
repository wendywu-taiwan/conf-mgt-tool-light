cd ..
cd ..
. venv/bin/activate
python manage.py init_conf apac
# python manage.py runserver 00.0.0.0:8020
nohup python manage.py runserver 00.0.0.0:8020 &