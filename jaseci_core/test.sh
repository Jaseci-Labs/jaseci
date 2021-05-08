export CLASSPATH="$PWD/jaseci/jac/antlr4-tool/antlr-4.9.2-complete.jar:$CLASSPATH"
java -Xmx500M -cp \"$PWD/jaseci/jac/antlr4-tool/antlr-4.9.2-complete.jar:$CLASSPATH\" org.antlr.v4.Tool -Dlanguage=Python3 -o $PWD/jaseci/jac/_jac_gen $PWD/jaseci/jac/jac.g4
python3 -m unittest discover jaseci/ && flake8 --exclude=settings.py,*migrations*,_jac_gen

