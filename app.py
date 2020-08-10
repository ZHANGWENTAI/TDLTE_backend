# -*- coding utf-8 -*-
import click
import time
import pyodbc as odbc
from flask import Flask, request, jsonify
from flask_cors import CORS
from db.initDB import initDB, initIndex
from handler import *
import processbar

app = Flask(__name__)
CORS(app, supports_credentials=True)

connection = odbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=TDLTE')

@app.cli.command()
def initdb():
    initDB()
    initIndex()
    click.echo('\nInitialized database.\n')

@app.cli.command()
def dbg():

    start1 = time.clock()
    handle_enodeb(enodeb_id='273991')
    end1 = time.clock()
    initIndex()
    start2 = time.clock()
    handle_enodeb(enodeb_id='273991')
    end2 = time.clock()
    print("无索引：", end1 - start1, "有索引：", end2 - start2)
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

@app.route('/processbar', methods=['GET'])
def percent():
    table = request.args.get('table')
    p = processbar.row

    if table == 'config':
        p /= 5505
    elif table == 'kpi':
        p /= 970
    elif table == 'prb':
        p /= 93025
    elif table == 'mro':
        p /= 875605

    return jsonify(
        percent= p * 100
    )

@app.route('/cell', methods=['GET'])
def cell_query():
    cell_id = request.args.get('cell_id')
    cell_name = request.args.get('cell_name')
    c = connection.cursor()

    code, msg, info = handle_cell(cell_id, cell_name)
    c.close()
    return jsonify(
        status=code,
        message=msg,
        result=info,
    )

@app.route('/enodeb', methods=['GET'])
def enodeb_query():
    enodeb_id = request.args.get('enodeb_id')
    enodeb_name = request.args.get('enodeb_name')

    code, msg, info = handle_enodeb(enodeb_id, enodeb_name)
    return jsonify(
        status=code,
        message=msg,
        result=info,
    )

@app.route('/kpi', methods=['GET'])
def kpi_query():
    sector_name = request.args.get('sector_name')
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    prop = request.args.get('prop')

    code, msg, info = handle_kpi_query(sector_name, start_time, end_time, prop)

    return jsonify(
        status=code,
        message=msg,
        result=info,
    )

@app.route('/prb_stat', methods=['POST'])
def prb_stat():
    code, msg= handle_prb_stat(request.json['dst_path'])

    return jsonify(
        status=code,
        message=msg,
    )

@app.route('/prb_query', methods=['GET'])
def prb_query():
    sector_name = request.args.get('sector_name')
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    granularity = request.args.get('granularity')
    prop = request.args.get('prop')

    code, msg, info = handle_prb_query(sector_name, start_time, end_time, granularity, prop)

    return jsonify(
        status=code,
        message=msg,
        result=info,
    )

@app.route('/export', methods=['POST'])
def export():
    code, msg = handle_export(request.json['tb_name'], request.json['format'], request.json['path'])

    return jsonify(
        status=code,
        message=msg
    )

@app.route('/c2i_analysis', methods=['GET'])
def c2i_analysis():
    code, msg, info = handle_c2i_analysis()

    return jsonify(
        status=code,
        message=msg,
        result=info
    )

@app.route('/overlay_analysis', methods=['POST'])
def overlay_analysis():
    code, msg, triple = handle_overlay_analysis(request.json['x'])

    return jsonify(
        status=code,
        message=msg,
        result=triple
    )