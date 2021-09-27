import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session

from werkzeug.exceptions import abort

import fev_module as fev

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    inv = conn.execute('SELECT * FROM inv').fetchall()
    conn.close()
    return render_template('index.html', inv=inv)

@app.route('/new_record', methods=['GET', 'POST'])
def new_record():

    if request.method == 'POST':
        suz = request.form['suz']
        client = request.form['client']
### test
        service = 0
        pe = request.form['pe']
        pe_if = request.form['pe_if']
        vid = request.form['vid']

        conn = get_db_connection()

        conn.execute('INSERT INTO inv (suz,client,service,pe,pe_if,vid) VALUES (?, ?, ?, ?, ?, ?)',
            (suz, client, service, pe, pe_if, vid)
            )

#DEBUG
        print("###DEBUG###: ", suz, client, service, pe, pe_if, vid)

        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return render_template('new_record.html')

@app.route('/find_empty_vlan', methods=('GET', 'POST'))
def find_empty_vlan():

    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['pass']
        host = request.form['pe']

        # get start vlan
        start_unit = 1010
        # get finish vlan
        end_unit = 2999
        # get available vlan from device
        used_vids_set = fev.get_used_vids_set(host, user, passwd)
        # checks units in range (start_unit, end_unit) and add available on device to set
        busy_set = fev.get_busy_units_in_range(used_vids_set, start_unit, end_unit)
        # get available VIDs list
        vids = fev.get_empty_units_list(busy_set, start_unit, end_unit)

        # pass available VIDs list to template
        return render_template('empty_vlan.html', vids=vids)

    else:
        return render_template('empty_vlan.html')

