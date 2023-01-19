# creates theboilerplate for a new module

MODULE_TYPE=$1
MODULE_NAME=$2

if [ -z "$MODULE_TYPE" ]; then
    echo "Module type not specified"
    exit 1
fi

if [ -z "$MODULE_NAME" ]; then
    echo "Module name not specified"
    exit 1
fi

if [ -d "$MODULE_TYPE/$MODULE_NAME" ]; then
    echo "Module $MODULE_NAME already exists"
    exit 1
fi

mkdir $MODULE_TYPE/$MODULE_NAME
echo "from .$MODULE_NAME import * # noqa" >> $MODULE_TYPE/$MODULE_NAME/__init__.py
echo >> $MODULE_TYPE/$MODULE_NAME/$MODULE_NAME.py
echo >> $MODULE_TYPE/$MODULE_NAME/.gitignore
echo >> $MODULE_TYPE/$MODULE_NAME/README.md
echo >> $MODULE_TYPE/$MODULE_NAME/requirements.txt

mkdir $MODULE_TYPE/$MODULE_NAME/tests
echo >> $MODULE_TYPE/$MODULE_NAME/tests/test_$MODULE_NAME.py
mkdir $MODULE_TYPE/$MODULE_NAME/tests/fixtures
echo >> $MODULE_TYPE/$MODULE_NAME/tests/fixtures/$MODULE_NAME.jac