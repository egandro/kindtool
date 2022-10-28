export UID=$(shell id -u)
export GID=$(shell id -g)

PYTHON_IMG?=python:3.10-slim
TEST_KINDTOOL_IMG=test-kindtool-dind

requirements:
	pip3 install -r requirements.txt

# this doen't work
test-dind: sdist
	DOCKER_BUILDKIT=1 docker build tests/docker -t $(TEST_KINDTOOL_IMG)
	docker run --rm --name kindtool-$@ \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $$(pwd)/dist:/dist \
		-it $(TEST_KINDTOOL_IMG)

run-kindtool-init:
	cd src && python3 -m kindtool init -d ../build

run-kindtool-up:
	if [ ! -d "./build/" ]; then cd src && python3 -m kindtool init -d ../build; fi
	cd src && python3 -m kindtool up -d ../build

run-kindtool-destroy:
	cd src && python3 -m kindtool destroy -d ../build

run-kindtool-destroy-force:
	cd src && python3 -m kindtool destroy -d ../build -f

run-kindtool-status:
	cd src && python3 -m kindtool status -d ../build

run-kindtool-get:
	cd src && python3 -m kindtool get internal_registry -d ../build

sdist:
	rm -rf dist
	rm -rf src/kindtool/__pycache__
	rm -rf src/kindtool.egg-info
	python3 setup.py sdist

## --user="${UID}:${GID}"
sdist-test: sdist
	docker run --rm --name kindtool-$@ -v $$(pwd)/dist:/dist -it $(PYTHON_IMG)  \
		/bin/sh -c 'pip --disable-pip-version-check install --root-user-action=ignore /dist/*.tar.gz && kindtool -v'

# https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3
package: sdist-test
	#pip3 install twine
	twine upload dist/*.tar.gz

dev-install: sdist
	pip3 uninstall kind || true
	pip3 install dist/*.tar.gz
