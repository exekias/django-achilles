SRC=achilles

sense: pep8 pyflakes test

test: test_python test_js

test_python:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=test_settings             \
	django-admin.py test --with-coverage --cover-package=achilles \
                         --cover-erase --cover-inclusive          \
                         --cover-branches --cover-tests

test_js:
	phantomjs $(SRC)/tests/run-qunit.js $(SRC)/tests/test.html?coverage=true

pep8:
	pep8 $(SRC)

pyflakes:
	pyflakes $(SRC)

clean:
	coverage erase
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist *.egg build
