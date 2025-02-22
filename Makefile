activate:
	source ./venv/bin/activate

dev:
	FLASK_APP=hook2shell.py flask run

build:
	docker build --tag hook2shell .

run:
	docker run -d -p 9080:9080 hook2shell
