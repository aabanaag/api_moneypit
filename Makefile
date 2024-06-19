# start services
start:
	docker-compose -f docker-compose.local.yml up --build

# stop services
stop:
	docker-compose -f docker-compose.local.yml stop

# build
build:
	docker-compose -f docker-compose.local.yml build

# start services detached
run:
	docker-compose -f docker-compose.local.yml up --build -d

# make migrations
makemigrations:
	docker-compose -f docker-compose.local.yml run --rm django python manage.py makemigrations

# migrate
migrate:
	docker-compose -f docker-compose.local.yml run --rm django python manage.py migrate

# create superuser
createsuperuser:
	docker-compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

# run test
test:
	docker-compose -f docker-compose.local.yml run --rm django pytest -s

# coverage
coverage:
	docker-compose -f docker-compose.local.yml run --rm django pytest --cov=. --cov-report=html

# create app
createapp:
	mkdir api_moneypit/$(app) && django-admin startapp $(app) api_moneypit/$(app)

# collectstatic
collectstatic:
	docker-compose -f docker-compose.local.yml run --rm django python manage.py collectstatic --noinput

