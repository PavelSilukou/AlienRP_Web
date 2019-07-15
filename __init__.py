#!/usr/bin/python

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 0
app.config['MYSQL_USER'] = 'apialienrpcom'
app.config['MYSQL_PASSWORD'] = 'q0sN3UjOIiJv'
app.config['MYSQL_DB'] = 'apialienrpcom'

mysql = MySQL(app)

def get_last_version():
    cur = mysql.connection.cursor()
    cur.execute("SELECT version_number FROM version ORDER BY id")
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None

def check_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE id = {}".format(user_id))
    row = cur.fetchone()
    if row:
        return True
    else:
        return False
		
def get_max_user_id():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(id) FROM user")
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None
		
def insert_new_user(user_id):
    cur = mysql.connection.cursor()
    insert = "INSERT INTO user(id) VALUES ({})".format(user_id)
    try:
        cur.execute(insert)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        return False
		
    return True
	
def insert_login_event(user_id, version_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM version WHERE version.version='{}'".format(version_name))
    row = cur.fetchone()
    version_id = 0
    if row:
        version_id = row[0]
    else:
        return None
		
    try:
        insert = "INSERT INTO login_event(user_id, version_id) VALUES ({}, {})".format(user_id, version_id)
        cur.execute(insert)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        return
		
def update_user(user_id, os_version, os_architecture):
    cur = mysql.connection.cursor()
    update = "UPDATE user SET os_version='{}', os_architecture='{}' WHERE id = {}".format(os_version, os_architecture, user_id)
    cur.execute(update)
    mysql.connection.commit()

@app.route('/login', methods=['POST'])
def login():
    while True:
        if not request.json or not 'alienrp_version' in request.json:
            abort(400)
        max_user_id = int(get_max_user_id()) + 1
        result = insert_new_user(max_user_id)
        if result:
            insert_login_event(max_user_id, request.json['alienrp_version'])
            return jsonify({'user_id': max_user_id}), 200
        else:
            continue
	
@app.route('/login/<int:user_id>', methods=['POST'])
def login_user_id(user_id):
    if not request.json or not 'alienrp_version' in request.json:
        abort(400)
    if check_user_id(user_id):
        insert_login_event(user_id, request.json['alienrp_version'])
        return "", 200
    else:
        abort(400)

@app.route('/user/<int:user_id>', methods=['POST'])
def set_user_data(user_id):
    if not request.json or not 'os_version' in request.json or not 'os_architecture' in request.json:
        abort(400)
		
    if check_user_id(user_id):
        update_user(user_id, request.json['os_version'], request.json['os_architecture'])
        return ""
    else:
        abort(400)

@app.route('/version', methods=['GET'])
def get_version():
    version_number = get_last_version()
    return jsonify({'version': version_number}), 200
    #return "true"