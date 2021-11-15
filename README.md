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

2. Install venv if not already installed:  
`pip install virtualenv`
  
3. Create an environment:  
`python3 -m venv ./`
  
Windows: `python -m venv venv`  

4. Activate environment  

macOS/Linux:  
`source venv/bin/activate`  

Windows:  
`.venv\Scripts\activate.bat`

5. Install flask  
`pip install flask`

5. Install libraries neccessary for MQTT
`pip install flask_mqtt flask_socketio eventlet`

5. Set environment value for development:
`export FLASK_ENV=development`

CMD:
`set FLASK_ENV=development`

PowerShell:
`$env:FLASK_ENV = "development"`

7. Initialize (or reinitialize) database:  
`flask init-db`

7. Run  
`flask run`

### Mosquitto instalation

Install and run [mosquitto](https://mosquitto.org/download/).
For this app, we will use the default configurations of mosquitto.

#### Mac

1. `brew install mosquitto`
2. If restarting the service is needed: `brew services restart mosquitto`
