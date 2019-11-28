from math import sqrt;
from itertools import count,islice
from flask import Flask, request
from flask_basicauth import BasicAuth
import subprocess
import socket
import psutil

def isPrime(n):
 return n > 1 and all(n%i for i in islice(count(2),int(sqrt(n)-1)))

def allPrime(max):
	num = 0
	result = "all prime number from 1 to " + str(max-1) + " = [ "
	while num < max:
		if(isPrime(num)):
			result = result + str(num) + ", "
		num = num + 1
	result = result[:-2]
	result += " ] \n"
	return result

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

basic_auth = BasicAuth(app)

@app.route("/prime/<num>",  methods=['POST'])
def prime(num):
	global userList
        userName = request.form['userName']
        password = request.form['password']
	for key, value in userList.iteritems() :
                if(userName == key and password == value ): 
			return allPrime(int(num))
     	return "you are not admin or user membre to use this url"

@app.route("/compute/usage")
@basic_auth.required
def compute():
        return "cpu: "+str(psutil.cpu_percent()) + "%   ,  ram: " + str(psutil.virtual_memory())

@app.route("/user/add",  methods=['POST'])
@basic_auth.required
def userAdd():
	global userList
	userName = request.form['userName']
	password = request.form['password']
	print(userName)
	#print(list(userList.keys()))
	if userName in userList.keys():
  		return "the user name already exsite in the database, try another user name."
	else:
		userList.update({userName : password})
  		return "user added with success."

@app.route("/user/list")
@basic_auth.required
def userList():
	global userList
	returnValue ="user list: \n"
	for key, value in userList.iteritems() :
		returnValue += key + ":" + value + "\n"
	return returnValue

userList = dict()
userList.update({ "admin" : "admin"})
#userList = { "admin" : "admin" }

app.run(host="0.0.0.0", port=2019)


