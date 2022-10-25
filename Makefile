PYTHON_IMG?=python:3.10-slim

requirements:
	pip3 install -r requirements.txt

sdist:
	rm -rf dist
	python3 setup.py sdist

sdist-test: sdist
	docker run --rm --name kind-sdist-test -v $$(pwd)/dist:/dist -it $(PYTHON_IMG)  \
		/bin/sh -c 'pip --disable-pip-version-check install --root-user-action=ignore /dist/*.tar.gz && kindtool -v'

# https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3
package: sdist-test
	#pip3 install twine
	twine upload dist/*