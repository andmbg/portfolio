env_activate = . env/bin/activate
python = $(env_activate) && python3

install: requirements.txt
	python3 -m venv env
	./env/bin/pip install -r requirements.txt

run: env/bin/activate
	$(python) -m app

