""" This module runs the api """
from v1.api import create_app

APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)
