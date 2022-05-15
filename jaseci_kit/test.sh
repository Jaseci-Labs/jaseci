if [ ! -z "$1" ]
then
    cd $1;
    python3 -m unittest discover . -p "test_*.py"
    flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app
else
    cd "jaseci_kit/modules"
    for MODEL in encoders entity_extraction fasttext
    do
        cd $MODEL
        python -m unittest discover . -p "test_*.py"
        cd ..
    done
    # flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app
fi
