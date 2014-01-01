SRC=achilles

sense: pep8 pyflakes test coverage

test: test_python test_js

test_python:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=test_settings  \
    coverage run --source=achilles --branch            \
                 `which django-admin.py` test

test_js:
	phantomjs $(SRC)/tests/run-qunit.js $(SRC)/tests/test.html?coverage=true

pep8:
	pep8 $(SRC)

pyflakes:
	pyflakes $(SRC)

coverage: test_python
	coverage report -m

doc:
	cd doc; make html

clean:
	coverage erase
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist *.egg build
	cd doc; make clean

.PHONY: doc
