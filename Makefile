.PHONY: all production docs test tests clean

all: production

production:
	@true

tests: test

test:
	tox

clean:
	rm -rf .tox
	rm -rf lfds.egg-info
	find lfds tests -name '*.pyc' -delete -or -name '*.pyo' -delete -or -name '__pycache__' -delete
