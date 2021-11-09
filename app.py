import os
from flask import Flask
import db
import auth
import environment
import headrest
import status
import sheet

test_config = None

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

@app.route('/')
def hello_world():
    return 'Hello World!'

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(environment.bp)
app.register_blueprint(headrest.bp)
app.register_blueprint(status.bp)
app.register_blueprint(sheet.bp)
