#!/bin/bash
PODN=jsuse
if [[ $1 ]]; then
    PODN=$1
fi

for podname in $(kubectl get pods -l pod=$PODN -o json| jq -r '.items[].metadata.name');
  do
    echo "Copy latest $PODN service.py and re-deploy it" | head -n 1;
    kubectl cp ai_serving ${podname}:/;
    kubectl exec -it ${podname} -- sh -c "pkill python";
    echo "Redeployed";
  done
