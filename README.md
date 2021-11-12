# SmartBed-RESTApi-Example

This application is an example of how to build a REST API. The application os a mock
IoT device, simulating a Smart Bed.
Implemented endpoints:

* Headrest adjustment (at the user's prefference)
* Detection of the bed sheet
* Retrieval of envrionment temperature

### Credits
This tutorial is based on the official Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/

### OpenAPI specification

You can check out tools that automate the generation of the specification like:
https://openap.is

### Instalation

You should have python3 installed and pip3. 

1. cd into this project  
  
2. Create an environment:  
`python3 -m venv ./`  

3. Activate environment
`source venv/bin/activate`

4. Install flask
`pip install flask`

5. Set environment value for development:
`export FLASK_ENV=development`

6. Run
`flask run`
