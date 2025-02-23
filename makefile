include .env

.PHONY: train  autopep8 isort flake8

#* Python Rules

RUN_SRC = src

server:
	python $(RUN_SRC)/server.py

client:
	python $(RUN_SRC)/client.py



#* Git Rules
isort:
	isort --settings-path=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

autoflake:
	autoflake --remove-all-unused-imports --in-place --recursive $(FORMAT_CHECK_SRC)

autopep8:
	autopep8 --in-place --recursive $(FORMAT_CHECK_SRC)

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE)  --recursive=y  $(FORMAT_CHECK_SRC)

flake8:
	flake8 --config=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

format: autoflake autopep8 isort

check: flake8 pylint

prepare-commit: autoflake autopep8 isort flake8 pylint