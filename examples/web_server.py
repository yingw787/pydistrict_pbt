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
db_path: str = os.path.join(os.path.dirname(__file__), "web_server.sqlite3")


@app.route("/init")
def init_db():
    # Ensure db/table will be fresh upon init
    if os.path.exists(db_path):
        os.remove(db_path)

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
        "data": {"type": "table", "name": "employees", "sql": response},
        "status": 200,
    }

    return json_response


@app.route("/test")
def write_sample_input_data():
    name = request.args.get("name")
    age = request.args.get("age")

    if name is None:
        json_response = {"status": 400, "error": "name not found"}
        return json_response
    if age is None:
        json_response = {"status": 400, "error": "age not found"}
        return json_response

    insert_sql_query = """
    INSERT INTO employees(id, name, age)
    VALUES (NULL, '{name}', {age});
    """.format(
        name=name, age=age
    )

    db_conn = sqlite3.connect(db_path)
    db_cursor = db_conn.cursor()

    try:
        db_cursor.execute(insert_sql_query)
        db_conn.commit()
    except sqlite3.IntegrityError as e:
        json_response = {
            "status": 400,
            "error": "Integrity failure upon data insertion",
        }
        return json_response

    get_sql_query = """
    SELECT * FROM employees
    WHERE id = {id}
    """.format(
        id=db_cursor.lastrowid
    )

    db_cursor.execute(get_sql_query)
    get_response = list(db_cursor.fetchone())
    db_cursor.close()
    db_conn.close()

    (resp_id, resp_name, resp_age) = get_response

    json_response = {
        "data": {"row_id": resp_id, "name": resp_name, "age": resp_age},
        "status": 200,
    }

    return json_response
