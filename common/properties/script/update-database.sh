cd ..
cd ..
cd ..
. venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations permission
python3 manage.py makemigrations common
python3 manage.py makemigrations RulesetComparer
python3 manage.py migrate permission
python3 manage.py migrate common
python3 manage.py migrate RulesetComparer
python3 manage.py migrate
