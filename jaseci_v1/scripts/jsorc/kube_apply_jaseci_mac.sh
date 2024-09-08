#! /opt/homebrew/bin/bash
echo "Deploying using namespace: $1"

env_vars=""
declare -A keyword_args=( [template]="jaseci-template" [POSTGRES_HOST]="jaseci-db" [DBNAME]="postgres" [JSORC_DB_REGEN]="\"true\"" [REDIS_HOST]="jaseci-redis")

for ARGUMENT in "${@:2}"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    KEY_LENGTH=${#KEY}
    keyword_args[$KEY]="${ARGUMENT:$KEY_LENGTH+1}"
done

file_name="${keyword_args[template]}"
unset keyword_args["template"]

sed "s/\$j{namespace}/$1/" $file_name > tmp-$file_name.yaml

for key in ${!keyword_args[@]}
do
    env_vars="${env_vars}\n            - name: ${key}\n              value: ${keyword_args[$key]}\n"
done

sed -i '' "s/\$j{env_vars}/${env_vars}/" tmp-$file_name.yaml

kubectl apply -f tmp-$file_name.yaml

echo "tmp-$file_name.yaml file will not be deleted for debugging"
