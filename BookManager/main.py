import os
import cherrypy
import django
import webview
import sys
import threading
import logging
from logging import handlers
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from time import sleep
from django.core.mail.backends import *

logger = logging.getLogger("BookManager.log")

class DjangoApplication(object):
    HOST = "127.0.0.1"
    PORT = 9090

    @staticmethod
    def mount_static(url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400,
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def start_ui(self):
        if self.url_ok(self.HOST, self.PORT):
            webview.create_window("Book Manager", "http://%s:%s" % (self.HOST, self.PORT),
                              width=1000, height=600, resizable=True, fullscreen=False, min_size=(900, 600))
        else:
            # wait for server to be up
            while not self.url_ok(self.HOST, self.PORT):
                sleep(0.1)

            webview.create_window("Book Manager", "http://%s:%s" % (self.HOST, self.PORT),
                                width=1000, height=600, resizable=True, fullscreen=False, min_size=(900, 600))

    @staticmethod
    def url_ok(url, port):
        try:
            from http.client import HTTPConnection
        except ImportError:
            from httplib2 import HTTPConnectionWithTimeout as HTTPConnection
        try:
            conn = HTTPConnection(url, port)
            conn.request("GET", "")
            r = conn.getresponse()
            return r.status == 200
        except:
            logger.exception("Server not started")
            return False

    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            'engine.autoreload_on': False,
            'log.screen': True,
            'log.access_file': cherry_access_log,
            'log.error_file': cherry_error_log,
        })
        self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)
        self.mount_static(settings.MEDIA_URL, settings.MEDIA_ROOT)

        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()


if __name__ == "__main__":
    # check if we are running as app bundle or script
    if getattr(sys, 'frozen', None):
        base_dir = os.path.realpath(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        run_as_binary = True
    else:
        base_dir = os.path.realpath(os.path.dirname(__file__))
        run_as_binary = False

    # setup logging and app_name
    if run_as_binary is True:
        log_file = os.path.join(base_dir, "..", "Coding_and_programming_project.log")
        cherry_access_log = os.path.join(base_dir, "..", "access.log")
        cherry_error_log = os.path.join(base_dir, "..", "log.log")
        app_name = "Book Manager"
    else:
        log_file = os.path.join(base_dir, "Coding_and_programming_project.log")
        cherry_access_log = os.path.join(base_dir, "access.log")
        cherry_error_log = os.path.join(base_dir, "log.log")
        app_name = "Python"

    log = logging.getLogger("Coding_and_coding_project")
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=30000000, backupCount=10)
    handler.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(fmt)
    log.addHandler(handler)

# Django settings  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookManager.settings')
    os.environ["DJANGO_SETTINGS_MODULE"] = "BookManager.settings"
    django.setup()
    DjangoApplication().run()

    # let web app run as background thread
    t = threading.Thread(target=DjangoApplication().start_ui())
    t.daemon = True
    t.start()

    # stop django when user closes UI
    cherrypy.engine.stop()