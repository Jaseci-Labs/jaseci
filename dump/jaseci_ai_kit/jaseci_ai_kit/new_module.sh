# creates the new jaseci_ai_kit module folder structure

MODULE_NAME=$1

if [ -z "$MODULE_NAME" ]; then
    echo "Usage: new_module.sh <module_name>"
    exit 1
fi

if [ -d "modules/$MODULE_NAME" ]; then
    echo "Module $MODULE_NAME already exists"
    exit 1
fi

echo "from jaseci_ai_kit.modules.$MODULE_NAME.$MODULE_NAME import * # noqa" >> $MODULE_NAME.py

mkdir modules/$MODULE_NAME
echo >> modules/$MODULE_NAME/__init__.py
echo >> modules/$MODULE_NAME/$MODULE_NAME.py
echo >> modules/$MODULE_NAME/.gitignore
echo >> modules/$MODULE_NAME/README.md
echo >> modules/$MODULE_NAME/requirements.txt

mkdir modules/$MODULE_NAME/tests
echo >> modules/$MODULE_NAME/tests/test_$MODULE_NAME.py
mkdir modules/$MODULE_NAME/tests/fixtures
echo >> modules/$MODULE_NAME/tests/fixtures/$MODULE_NAME.jac