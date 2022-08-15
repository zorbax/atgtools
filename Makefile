.PHONY: all lint test install dev clean distclean

PYTHON ?= python
PREFIX ?= $(CONDA_PREFIX)

all: ;

lint:
	mypy
	flake8

test: all
	ATGTEST= pytest

test_atg: all
	MYSTERY_STEW= pytest -k test_atg -n auto

install: all
	$(PYTHON) setup.py install && \
	mkdir -p $(PREFIX)/etc/conda/activate.d && \
	cp bin/activate_q2cli_tab_completion.sh $(PREFIX)/etc/conda/activate.d/

