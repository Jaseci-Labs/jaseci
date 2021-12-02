#!/bin/bash
# This script set ups the scaffoldings required for setting up a new AI service
# It uses the various files in the template/ directory

if [ $# -ne 1 ]; then
    echo "Usage: ./create_ai_service.sh {AIServiceName}. Make sure the name you provide is in CamelCase"
    exit 1
fi

CamelCaseName=$1
SnakeCaseName=$(echo "${CamelCaseName}" | sed 's/\([^A-Z]\)\([A-Z0-9]\)/\1_\2/g' | sed 's/\([A-Z0-9]\)\([A-Z0-9]\)\([^A-Z]\)/\1_\2\3/g' | tr '[:upper:]' '[:lower:]')
DashName=$(sed s/_/-/g <<<${SnakeCaseName})

if [ -d $SnakeCaseName ]; then
    echo "Error: $SnakeCaseName already exists."
    exit 1
fi

# Copy template files over
mkdir ${SnakeCaseName}
cp template/Dockerfile ${SnakeCaseName}/Dockerfile
cp template/requirements.txt ${SnakeCaseName}/requirements.txt
cp template/jaseci_ai_service.py ${SnakeCaseName}/${SnakeCaseName}.py
cp template/jaseci_ai_service.yaml ${SnakeCaseName}/${SnakeCaseName}.yaml

# Replace the placeholder name in the flask app file and yaml file
sed -i "s/JaseciAIService/${CamelCaseName}/g" ${SnakeCaseName}/${SnakeCaseName}.py
sed -i "s/jaseci-ai-service/${DashName}/g" ${SnakeCaseName}/${SnakeCaseName}.yaml
sed -i "s/jaseci_ai_service/${SnakeCaseName}/g" ${SnakeCaseName}/${SnakeCaseName}.yaml
sed -i "s/JaseciAIService/${CamelCaseName}/g" ${SnakeCaseName}/${SnakeCaseName}.yaml

# Next steps
echo -e "The new app ${CamelCaseName} is ready for development."
echo -e "Here are the next steps:"
echo -e "1. Add steps in ${SnakeCaseName}/Dockerfile to download and prepare any pre-trained model files. Follow the TODOs."
echo -e "2. Update ${SnakeCaseName}/requirements.txt with python dependencies required for your model."
echo -e "3. Fill in the rest of the code in the service code in ${SnakeCaseName}/${SnakeCaseName}.py. Follow the TODOs."
echo -e "4. Take a look at the k8s manifest at ${SnakeCaseName}/${SnakeCaseName}.yaml". You might need to update the memory limit and/or port.
echo -e "5. Build the docker image with \"cd ${SnakeCaseName} && docker build -t ${DashName} -f Dockerfile\""
echo -e "6. Finally, test the service by applying the manifest \"kubectl apply -f ${SnakeCaseName}.yaml\""
