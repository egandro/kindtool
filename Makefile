requirements:
	pip3 install -r requirements.txt

sdist:
	rm -rf dist
	python3 setup.py sdist

# https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3
package: sdist
	#pip3 install twine
	twine upload dist/*