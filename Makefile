.PHONY: flake8 test ship


flake8:
	flake8 pybns


test:
	python setup.py test


ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
