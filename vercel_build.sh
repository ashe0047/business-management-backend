pip install -r requirements.txt
python3.9 manage.py migrate --noinput
python3.9 manage.py collectstatic --noinput
python3.9 manage.py initroles
python3.9 manage.py initsuperuser