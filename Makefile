.PHONY: doc
.PHONY: test

doc:
	sphinx-apidoc -o doc/source src
	make html -C doc

install:
	pip3 install -r requirements.txt

clean:
	@rm -rf *.pyc
	@rm -rf __pycache__

test:
	python -m unittest discover -s test

