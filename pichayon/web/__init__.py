__version__ = "0.0.1"


from flask import Flask, request, abort, Response

from . import views
from . import acl
from . import oauth2
from .client import nats_client
from .client import pichayon_client
from .. import models


def create_app():
    app = Flask(__name__)
    app.config.from_object("pichayon.default_settings")
    app.config.from_envvar("PICHAYON_SETTINGS", silent=True)

    models.init_db(app)
    acl.init_acl(app)
    oauth2.init_oauth(app)

    views.register_blueprint(app)
    nats_client.nats_client.init_app(app)
    pichayon_client.init_client(nats_client.nats_client)
    return app
