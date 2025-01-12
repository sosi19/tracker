from api import app
from flask_serverless import FlaskServerless

handler = FlaskServerless(app)

def handler(event, context):
    print("Evento recebido:", event)
    return handler.handle(event, context) 