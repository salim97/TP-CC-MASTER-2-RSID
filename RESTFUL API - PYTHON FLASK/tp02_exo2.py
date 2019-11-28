from flask import Flask, request
from flask_basicauth import BasicAuth
import subprocess
import socket


#from flask import request
from datetime import datetime
now = datetime.now() # current date and time

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

basic_auth = BasicAuth(app)

@app.route("/ifconfig")
@basic_auth.required
def ifconfig():
	proc = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	tmp = proc.stdout.read()
	return tmp


@app.route("/ifaces")
@basic_auth.required
def ifaces():
	p = subprocess.Popen('ls /sys/class/net',
                     	shell=True,
                     	stdout=subprocess.PIPE,
        	        stderr=subprocess.PIPE)
	out, err = p.communicate()
#        tmp = proc.stdout.read()
        return out


@app.route("/ip/<iface>")
@basic_auth.required
def getIP(iface):
        p = subprocess.Popen("ip -4 addr show "+iface+" | grep -oP '(?<=inet\s)\d+(\.\d+){3}'",
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        out, err = p.communicate()
	return out

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


@app.route("/ip/<iface>",  methods=['POST'])
@basic_auth.required
def setIP(iface):
	isIPvalid = is_valid_ipv4_address(request.form['ip'])
	print(isIPvalid)
	if(isIPvalid):
		return request.form['ip'] + " is a valid IP"
	else:
		return request.form['ip'] + " is not a valid IP"

@app.route("/dns/<iface>")
@basic_auth.required
def getDNS(iface):
        p = subprocess.Popen("nmcli device show  "+iface+" | grep IP4.DNS",
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out



app.run(host="0.0.0.0", port=2019)

