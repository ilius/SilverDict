import logging

from app import create_app
from waitress import serve

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
	app = create_app()
	serve(app, listen='{}:{}'.format(app.extensions['dictionaries'].settings.preferences['listening_address'], app.extensions['dictionaries'].settings.PORT))
