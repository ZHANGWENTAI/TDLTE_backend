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

@app.cli.command()
def dbg():
    code, msg, res = handle_prb_query(connection.cursor(),
                                    '三门峡连霍义马高速东-HLHF-1',
                                    '07/17/2016 00:00:00',
                                    '07/19/2016 00:00:00',
                                    1, 'prb60')
    print(msg)
    print(res)
    click.echo('\nOK.\n')

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

@app.route('/cell', methods=['GET'])
def cell():
    cell_id = request.args.get('cell_id')
    cell_name = request.args.get('cell_name')

    code, msg, info = handle_cell(cell_id, cell_name)
    return jsonify(
        status=code,
        message=msg,
        data=info,
    )

@app.route('/enodeb', methods=['GET'])
def enodeb():
    enodeb_id = request.args.get('enodeb_id')
    enodeb_name = request.args.get('enodeb_name')

    code, msg, info = handle_enodeb(enodeb_id, enodeb_name)
    return jsonify(
        status=code,
        message=msg,
        data=info,
    )

# @app.route('/kpi', methods=['GET'])
# def kpi():
#     cell_name = request.args.get('cell_name')
#     start_time = request.args.get('from')
#     end_time = request.args.get('to')
#     props = request.args.get('props')
#
#     code, msg, info = handle_kpi_query(cell_name, start_time, end_time, props)
#
#     return jsonify(
#         status=code,
#         message=msg,
#         data=info,
#     )

@app.route('/prb_stat', methods=['POST'])
def prb_stat():
    code, msg, info = handle_prb_stat(request.json['src_path'], request.json['dst_path'])

    return jsonify(
        status=code,
        message=msg,
        data=info,
    )

@app.route('/prb_query', methods=['GET'])
def prb_query():
    cell_name = request.args.get('cell_name')
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    props = request.args.get('props')

    code, msg, info = handle_prb_query(cell_name, start_time, end_time, props)

    return jsonify(
        status=code,
        message=msg,
        data=info,
    )

@app.route('/export', methods=['POST'])
def export():
    code, msg = handle_export(request.json['tb_name'], request.json['format'], request.json['path'])

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/overlay', methods=['GET'])
def overlay():
    code, msg = handle_overlay_analysis()

    return jsonify(
        status=code,
        message=msg
    )