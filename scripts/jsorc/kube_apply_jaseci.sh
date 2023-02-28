echo "Deploying using namespace: $1"
sed "s/\$j{namespace}/$1/" jaseci-template > tmp.jaseci.yaml

env_vars=""
for ARGUMENT in "${@:2}"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    KEY_LENGTH=${#KEY}
    VALUE="${ARGUMENT:$KEY_LENGTH+1}"
    env_vars="${env_vars}\n            - name: ${KEY}\n              value: ${VALUE}"
done

sed -i "s/\$j{env_vars}/${env_vars}/" tmp.jaseci.yaml

kubectl apply -f tmp.jaseci.yaml

echo "tmp.jaseci.yaml file will not be deleted for debugging"
