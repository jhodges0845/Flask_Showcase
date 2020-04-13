from flask import Flask
from home.routes import home_view

def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(home_view)
    return app

app = create_app('config.py')

    #Run Server... runing on Port 5000#
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
