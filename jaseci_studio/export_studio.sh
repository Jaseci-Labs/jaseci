yarn build
rm -rf sandbox
rm -rf ../jaseci_serv/templates/studio
rm -rf ../jaseci_serv/static/studio
mkdir sandbox sandbox/templates sandbox/static
mkdir ../jaseci_serv/templates/studio ../jaseci_serv/static/studio
# move all files ending with .html from dist folder to sandbox folder
mv dist/*.html ../jaseci_serv/templates/studio
mv dist/* ../jaseci_serv/static/studio
python3 format_templates.py -d ../jaseci_serv/templates/studio
