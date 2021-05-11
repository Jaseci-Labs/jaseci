export CLASSPATH="antlr4-tool/antlr-4.9.2-complete.jar:$CLASSPATH"
java -Xmx500M -cp \"antlr4-tool/antlr-4.9.2-complete.jar:$CLASSPATH\" org.antlr.v4.Tool -Dlanguage=Python3 -o jac_parse jac.g4
touch jac_parse/__init__.py;
