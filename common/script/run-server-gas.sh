cd ..
cd ..
cd ..
. venv/bin/activate
python manage.py init_conf gas
python manage.py runserver 00.0.0.0:8022
# nohup python manage.py runserver 00.0.0.0:8021 &