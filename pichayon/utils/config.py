import os
import logging
import flask

logger = logging.getLogger(__name__)

settings = None


def get_settings():
    global settings

    if not settings:
        filename = os.environ.get("PICHAYON_SETTINGS", None)

        if filename is None:
            logger.error("This program require PICHAYON_SETTINGS environment")
            return
        logger.debug(filename)

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")

        settings = flask.config.Config(file_path)
        settings.from_object("pichayon.default_settings")
        settings.from_envvar("PICHAYON_SETTINGS", silent=True)

    return settings
