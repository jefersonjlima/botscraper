.PHONY: help prepare-dev run schedule_scraper clean docker

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       prepare development environment"
	@echo "make run_pci"
	@echo "       run BotScraper PCI Contest"
	@echo "make docker"
	@echo "       mount docker"
prepare-dev:
	sudo apt-get -y install python3 python3-pip
	python3 -m pip install virtualenv
	make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .  --upgrade --ignore-installed
	touch $(VENV_NAME)/bin/activate

test: venv
	${PYTHON} -m pytest -vv tests

lint: venv
	${PYTHON} -m pylint botscraper

run: venv
	@${PYTHON} ./src/main.py

schedule_scraper:
	@echo "Scraper was scheduled"
		# * * * * * command to be executed
		# - - - - -
		# | | | | |
		# | | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
		# | | | ------- Month (1 - 12)
		# | | --------- Day of month (1 - 31)
		# | ----------- Hour (0 - 23)
		# ------------- Minute (0 - 59)
	# #write out current crontab
	@crontab -l > mycron
	# #echo new cron into cron file
	@echo "*/1 * * * * $(USER) python3 $(PWD)/src/main.py" >> mycron
	# #install new cron file
	@crontab mycron
	@rm mycron

clean:
	@rm -rf $(VENV_NAME) *.eggs *.egg-info .cache .mypy_cache/ .pytest_cache/ *.log

docker:
	@echo 'shall be included docker process'
