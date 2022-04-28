if [ ! -z "$1" ]
then
    cd $1;
    python3 -m unittest discover . -p "test_*.py"
    flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app --max-line-length=88 --extend-ignore = E203,
else
    for MODEL in encoders entity_extraction fasttext text_segmenter use_enc use_qa
    do
        cd $MODEL
        python3 -m unittest discover . -p "test_*.py"
        cd ..
    done
    flake8 --exclude=settings.py,*migrations*,jac_parse,ci_app --max-line-length=88 --extend-ignore = E203,
fi
