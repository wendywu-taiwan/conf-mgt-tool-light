cd ..
cd ..
. venv/bin/activate
python manage.py init_conf nl
nohup python manage.py runserver 00.0.0.0:8021 &