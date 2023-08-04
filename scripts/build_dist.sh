# pip install setuptools wheel twine
python3 setup.py sdist bdist_wheel
twine upload dist/*