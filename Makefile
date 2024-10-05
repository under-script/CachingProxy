gen-env:
	python3 -m venv env && . env/bin/activate
migrate:
	python3 manage.py migrate
run:
	python3 manage.py runserver
	#$(port)
i:
	pip install -r requirements/$(file_name).txt
freeze:
	pip freeze > requirements/$(file_name).txt
cru:
	python manage.py createsuperuser
# --username $(username) --email $(email)
migration:
	python3 manage.py makemigrations
create-not-author:
	python manage.py createuser --username notauthor --email notauthor@example.com --password 1
create-author:
	python manage.py createuser --username author --email author@example.com --password 1
collect:
	python manage.py collectstatic --noinput
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
startapp:
	python manage.py startapp $(name)