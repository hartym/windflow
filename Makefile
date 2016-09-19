# This file has been auto-generated.
# All changes will be lost, see Projectfile.
#
# Updated at 2016-09-18 19:27:38.495828

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
PYTHON_REQUIREMENTS_DEV_FILE ?= requirements-dev.txt
QUICK ?= 
VIRTUAL_ENV ?= .virtualenv-$(PYTHON_BASENAME)
PIP ?= $(VIRTUAL_ENV)/bin/pip
PYTEST_OPTIONS ?= --capture=no --cov=windflow --cov-report html
SPHINX_OPTS ?= 
SPHINX_BUILD ?= $(VIRTUAL_ENV)/bin/sphinx-build
SPHINX_SOURCEDIR ?= doc
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build

.PHONY: clean doc install install-dev lint test

# Installs the local project dependencies.
install: $(VIRTUAL_ENV)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ur $(PYTHON_REQUIREMENTS_FILE) ; \
	fi

# Installs the local project dependencies, including development-only libraries.
install-dev: $(VIRTUAL_ENV)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ur $(PYTHON_REQUIREMENTS_DEV_FILE) ; \
	fi

# Cleans up the local mess.
clean:
	rm -rf build
	rm -rf dist

# Setup the local virtualenv, or use the one provided by the current environment.
$(VIRTUAL_ENV):
	virtualenv -p $(PYTHON) $(VIRTUAL_ENV)
	$(PIP) install -U pip\>=8.1.2,\<9 wheel\>=0.29,\<1.0
	ln -fs $(VIRTUAL_ENV)/bin/activate activate-$(PYTHON_BASENAME)

lint: install-dev
	$(VIRTUAL_ENV)/bin/pylint --py3k windflow -f html > pylint.html

test: install-dev
	$(VIRTUAL_ENV)/bin/py.test $(PYTEST_OPTIONS) tests

doc: install-dev
	$(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html
