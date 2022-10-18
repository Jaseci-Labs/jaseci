python3 -m unittest discover jaseci -p "test_$1*.py" && flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app --max-line-length=88 --extend-ignore=E203
