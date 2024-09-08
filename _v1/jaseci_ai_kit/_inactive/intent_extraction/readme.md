Intent classification & Entity Extraction
This module is about classifying intent and tagging entities provided a text

Installation
Install the dependency provided in requirements.txt

Usage
1. start the application by :
    Uvicorn {name of the file(app)}:{name of the fastapi object(app)} -port {give a port no (default port 8000)}
2. Check the available API's by opening /docs in the browser
    e.g.: {http://localhost:8000}/docs
3. Make a call to desired API
    e.g. : {http://localhost:8000}/intentclassification
    Please provide the required parameters
