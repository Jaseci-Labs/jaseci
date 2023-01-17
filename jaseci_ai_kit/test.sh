for file in $(find . -name "test_$1*.py"); do
    if [[ $file == *_inactive* ]]; then
        continue
    fi
    echo "running $file"
    pytest --exitfirst -v $file
    if [ $? -ne 0 ]; then
        echo $file Failed
        exit 1
        break
    fi
done
