# -*- coding utf-8 -*-
import click
import pyodbc as odbc
from flask import Flask, request, jsonify
from flask_cors import CORS
from db.initDB import initDB
from handler import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

connection = odbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=TDLTE')

@app.cli.command()
def initdb():
    initDB()
    click.echo('\nInitialized database.\n')

@app.route('/register', methods=['POST'])
def register():
    c = connection.cursor()
    req = request.json
    result = handle_register(req['account'], req['authentication'], c)
    c.close()

    return jsonify(
        status=0 if result else 1,
        message='this account has existed'
    )

@app.route('/login', methods=['POST'])
def login():
    c = connection.cursor()
    code, msg = handle_login(request.json['account'], request.json['authentication'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg,
    )

@app.route('/config', methods=['POST'])
def config():
    c = connection.cursor()
    code, msg = handle_config(request.json['path'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/kpi', methods=['POST'])
def kpi():
    c = connection.cursor()
    code, msg = handle_kpi(request.json['path'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/prb', methods=['POST'])
def prb():
    c = connection.cursor()
    code, msg = handle_prb(request.json['path'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/mro', methods=['POST'])
def mro():
    c = connection.cursor()
    code, msg = handle_mro(request.json['path'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/export', methods=['POST'])
def export():
    c = connection.cursor()
    code, msg = handle_export(request.json['tbname'], request.json['format'], request.json['path'], c)
    c.close()

    return jsonify(
        status=code,
        message=msg
    )
