from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, _password):
    return username

@app.route('/')
@auth.login_required
def index():
    return {"Hello": auth.current_user()}

if __name__ == '__main__':
    app.run()
