python3 -m unittest discover jaseci_core/jaseci/ --failfast -p "test_$1*.py" && flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app
