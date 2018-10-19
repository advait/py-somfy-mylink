# Make the distribution archives
dist :
	python3 setup.py sdist bdist_wheel

# Upload dist to test pypi
twine.test : dist
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload dist to prod pypi
twine.prod :
	python3 -m twine upload dist/*

clean :
	rm -rf build/ dist/ somfy_mylink.egg-info/
