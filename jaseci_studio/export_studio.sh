yarn build
rm -rf sandbox
mkdir sandbox sandbox/templates sandbox/static
# move all files ending with .html from dist folder to sandbox folder
mv dist/*.html sandbox/templates
mv dist/* sandbox/static
python format_templates.py -d sandbox/templates