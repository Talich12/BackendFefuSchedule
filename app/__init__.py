from flask import Flask
from config import Config
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
ma = Marshmallow(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

spec = APISpec(
    title="Gisty",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="A minimal gist API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)

from app import models
from app.routes import routes, teacher, auditorium, discipline, pair_number