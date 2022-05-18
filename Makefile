SHELL := /bin/bash

mkfile_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: setup
setup:
	stat venv/bin/activate &> /dev/null || \
	python3 -m venv venv
	source venv/bin/activate; \
	pip install -r requirements.txt

.PHONY: install
install:
	sudo sed "s|{{DIR}}|$(mkfile_dir)|g" \
		labelcommander.service \
		> /lib/systemd/system/labelcommander.service
	sudo chmod 644 /lib/systemd/system/labelcommander.service
	sudo systemctl daemon-reload
	sudo systemctl enable labelcommander.service
	sudo systemctl start labelcommander
	sudo systemctl status labelcommander

.PHONY: uninstall
uninstall:
	sudo systemctl stop labelcommander
	sudo systemctl disable labelcommander.service
	sudo rm /lib/systemd/system/labelcommander.service
	sudo systemctl daemon-reload

.PHONY: run
run:
	source venv/bin/activate; \
	source env.sh; \
	python run.py
