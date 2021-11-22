from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import json
import time

import db
import auth
import environment
import headrest
import status_api
import sheet
import status

# Necessary monkey-patch
eventlet.monkey_patch()

app = None
mqtt = None
socketio = None
thread = None

def create_app():
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    @app.route('/')
    def hello_world():
        # Here I chose to start the periodic publishing after the root endpoint is called.
        # It's not the best nor cleaneste approach, but will have to refactor it. 
        # What is important is that the background_thread function is called on 
        # a separate thread, so that publishing can happen while simultaneously
        # HTTP endpoints are also functional.

        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return 'Hello World!'

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(headrest.bp)
    app.register_blueprint(status_api.bp)
    app.register_blueprint(sheet.bp)

    return app

def create_mqtt_app():

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio 
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt

def get_socketio_app():
    if socketio is None:
        create_app()
        create_mqtt_app()
    return socketio

def get_flask_app():
    if app is None:
        print("App was None")
        create_app()
        print("App is now not None")
    print("App is called")
    return app

# Start MQTT publishing

# Function that every second publishes a message
def background_thread():
    count = 0
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
        # Publish
        mqtt.publish('python/mqtt', message)

# App will now have to be run with `python app.py` as flask is now wrapped in socketio.
# The following makes sure that socketio is also used

def run_socketio_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_socketio_app()
    