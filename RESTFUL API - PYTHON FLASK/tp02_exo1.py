from flask import Flask, request
from flask_basicauth import BasicAuth

#from flask import request
from datetime import datetime
now = datetime.now() # current date and time

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

basic_auth = BasicAuth(app)

@app.route("/")
@basic_auth.required
def hello_world():
	return "Hello World"


@app.route("/time")
def time():
        return date_time

@app.route("/string/<string>")
def print_string(string):
        return string

@app.route("/string2",  methods=['POST'])
def print_form():
	print(request.form['msg'])
        return request.form['msg']


app.run(host="0.0.0.0", port=2019)

