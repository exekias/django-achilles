SRC=achilles

sense: pep8 pyflakes test

test: test_python test_js

test_python:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=test_settings  \
    coverage run --source=achilles --branch            \
                 `which django-admin.py` test
	coverage report -m

test_js:
	COVERAGE_REPORT=1 mocha -u tdd -R spec \
                            achilles/tests/test_javascript.js --coverage
	# Save lcov for later
	@mocha -u tdd -R json-cov \
           achilles/tests/test_javascript.js --coverage > .coverage-js

pep8:
	pep8 $(SRC)

pyflakes:
	pyflakes $(SRC)

doc:
	cd doc; make html

clean:
	coverage erase
	rm .coverage-js || true
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist *.egg build
	cd doc; make clean

.PHONY: doc
