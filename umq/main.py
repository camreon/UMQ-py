import os
from umq.app import create_app

DEBUG = os.environ.get('DEBUG') or False

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=DEBUG)

