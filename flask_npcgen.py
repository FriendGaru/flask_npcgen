"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
flask_app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = flask_app.wsgi_app

from routes import *

# if __name__ == '__main__':
#     import os
#     HOST = os.environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(os.environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     flask_app.run(HOST, PORT)

if __name__ == '__main__':

    flask_app.run()