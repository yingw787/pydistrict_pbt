#!/usr/bin/env python3
#
# This file defines a basic web server, the basic scaffold of what you might
# find at a small company or internal tools team. It exposes a REST API endpoint
# to make a database call.

import os

from flask import Flask
from flask import request
import sqlite3


app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "web_server.sqlite3")


@app.route("/init")
def init_db():
    db_conn = sqlite3.connect(db_path)

    create_table_sql_query = """
    CREATE TABLE IF NOT EXISTS employees
    (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT CHECK(length(name) >= 0),
        age INT CHECK(age >= 18)
    )
    """

    db_conn.execute(create_table_sql_query)

    describe_table_sql_query = """
    SELECT sql FROM sqlite_master
    WHERE name = 'employees'
    AND type = 'table'
    """

    response = list(db_conn.execute(describe_table_sql_query))[0][0]
    db_conn.close()

    json_response = {
        'data': {
            'type': 'table',
            'name': 'employees',
            'sql': response
        },
        'status': 200
    }

    return json_response


@app.route("/test")
def write_sample_input_data():
    name = request.args.get("name")
    age = request.args.get("age")

    if name is None:
        json_response = {
            "status": 400,
            "error": "name not found"
        }
        return json_response
    if age is None:
        json_response = {
            "status": 400,
            "error": "age not found"
        }
        return json_response

    sql_query = """
    INSERT INTO employees(name, age)
    VALUES ({name} {age});
    """.format(
        name=name,
        age=age
    )

    db_conn = sqlite3.connect(db_path)

    db_conn.execute(sql_query)

    db_conn.close()
