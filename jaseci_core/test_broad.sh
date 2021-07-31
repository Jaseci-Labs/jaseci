python3 -m unittest discover jaseci/ --failfast -p "test_*.py" -p "unit_test_*.py" && flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app

