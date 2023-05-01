#!/usr/bin/env python3
 
from flask import Flask, render_template, request, Response,jsonify
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
from flask_bootstrap import Bootstrap
from auth import getTicket

import os

DEBUG=True

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
@requires_authentication
def home(user):
	return jsonify(user)

@app.route('/negotiate')
def negotiate():
	headers = getTicket()
	return jsonify(headers)


if __name__ == '__main__':
	init_kerberos(app,service='host',hostname='server.example.tn')
	app.run(host='0.0.0.0',port=8080)
