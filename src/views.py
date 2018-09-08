from . import application


@application.route('/')
def index():
    return 'Hello, World!'
