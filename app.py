from flask import Flask
from helpers.exceptions import JSONExceptionHandler
from routes import routes

app = Flask(__name__)
handler = JSONExceptionHandler(app)
routes.init(app)

if __name__ == '__main__':
    app.run(DEBUG=False)
