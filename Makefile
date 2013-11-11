SRC=achilles

sense: pep8 pyflakes test

test: test_python test_js

test_python:
	DJANGO_SETTINGS_MODULE=test_settings coverage run --source=achilles \
                                         setup.py nosetests

test_js:
	phantomjs $(SRC)/tests/run-qunit.js $(SRC)/tests/test.html?coverage=true

pep8:
	pep8 $(SRC)

pyflakes:
	pyflakes $(SRC)
