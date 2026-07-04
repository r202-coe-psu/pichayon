import asyncio
import json
import threading

from nats.aio.client import Client as NATS

import logging

logger = logging.getLogger(__name__)


class NatsClient:
    """NATS client for the web app.

    The connection lives on a dedicated event loop running in a daemon
    thread, so it survives across requests. publish/request are plain
    sync methods that bridge onto that loop with run_coroutine_threadsafe,
    so views stay sync and work under any WSGI server (uwsgi, gunicorn,
    livereload/tornado).
    """

    def __init__(self, app=None):
        self.app = app
        self.nc = None
        self.loop = None
        self.thread = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(
            target=self.loop.run_forever, name="nats-client-loop", daemon=True
        )
        self.thread.start()

        self.nc = NATS()
        asyncio.run_coroutine_threadsafe(
            self.nc.connect(
                app.config.get("PICHAYON_MESSAGE_NATS_HOST"),
                max_reconnect_attempts=-1,
                reconnect_time_wait=2,
            ),
            self.loop,
        )

    def stop(self):
        if self.nc and self.loop:
            try:
                asyncio.run_coroutine_threadsafe(self.nc.drain(), self.loop).result(
                    timeout=5
                )
            except Exception as e:
                logger.exception(e)
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def publish(self, topic: str, message: dict):
        # logger.debug(f"publish -> {topic} => {message}")
        future = asyncio.run_coroutine_threadsafe(
            self.nc.publish(topic, json.dumps(message).encode()), self.loop
        )
        future.result(timeout=5)

    def request(self, topic: str, message: dict):
        # logger.debug(f"request -> {topic} => {message}")
        future = asyncio.run_coroutine_threadsafe(
            self.nc.request(topic, json.dumps(message).encode(), timeout=1), self.loop
        )
        msg = future.result(timeout=5)
        return json.loads(msg.data.decode())


nats_client = NatsClient()
