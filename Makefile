
rm:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf proxy.py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets
	

test: rm
	pytest -s -v  tests/

coverage-html:
	# --cov where you want to cover
	#  tests  where your test code is 
	pytest --cov=lee/ --cov-report=html tests/
	open htmlcov/index.html

coverage:
	pytest --cov=lee/ tests/

main:
	python -m src.main

install: uninstall
	sudo pip install . 

uninstall:
	sudo pip uninstall lee

run:
	lee 2
	python -m lee 2
	

all: rm uninstall install run 


pure-all: env-rm rm env install test run


	
upload-to-test: rm  
	python setup.py bdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: rm  
	python setup.py bdist
	twine upload dist/*


freeze:
	# pipreqs will find the module the project really depneds
	pipreqs . --force

freeze-global:
	#  pip will find all the module not belong to standard  library
	pip freeze > requirements.txt


env-rm:
	rm -rdf env


env:
	python3 -m venv env
	. env/bin/activate

