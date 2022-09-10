import logging
from posixpath import sep
import threading

from flask import Flask

from .blueprints import api_routes

logger = logging.getLogger(__name__)

class ThreadedFlaskApp:
    """Wrapper for a Flask object that simply allows abstraction of the run process such that it is run on a reperate thread"""
    def __init__(self, app):
        self.app = app
    
    def _start(self, host, port):
        """Abstraction of the .run() function, technically not needed, as you could just point target to self.app.run, but it's good to visualise what's going on."""
        self.app.run(host=host, port=port)

    def run(self, host, port) -> None:
        """Function to start the Flask App on a thread, just an abstraction of the .run() function"""
        logging.info("Starting Kafka Consumer thread")
        t = threading.Thread(target=self._start,kwargs={'host': host, 'port': port})
        t.start()

def create_app(seperate_thread=False):
    app = Flask(__name__)
    app.register_blueprint(api_routes)
    if seperate_thread:
        app.use_reloader=False
        app = ThreadedFlaskApp(app)
    return app

