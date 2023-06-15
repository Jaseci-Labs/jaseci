echo "Deploying using namespace: $1"
sed "s/\$j{namespace}/$1/" jaseci-template-exp > tmp.jaseci.yaml

env_vars=""
declare -A keyword_args=( [POSTGRES_HOST]="jaseci-db" [DBNAME]="postgres" [JSORC_DB_REGEN]="\"true\"" [REDIS_HOST]="jaseci-redis" [PROME_HOST]="jaseci-prometheus-server" [ELASTIC_HOST]="jaseci-es-http")

for ARGUMENT in "${@:2}"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    KEY_LENGTH=${#KEY}
    keyword_args[$KEY]="${ARGUMENT:$KEY_LENGTH+1}"
done

for key in ${!keyword_args[@]}
do
    env_vars="${env_vars}\n            - name: ${key}\n              value: ${keyword_args[$key]}\n"
done

sed -i "s/\$j{env_vars}/${env_vars}/" tmp.jaseci.yaml

kubectl apply -f tmp.jaseci.yaml

echo "tmp.jaseci.yaml file will not be deleted for debugging"
