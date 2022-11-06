for file in $(find jaseci_ai_kit/ -name "test_$1*.py"); do
    echo "running $file"
    pytest --exitfirst -v $file
    if [ $? -ne 0 ]; then
        echo $file Failed
        exit 1
        break
    fi
done
