# Back End Full_Stack App
from flask import Flask, request, jsonify
import sqlite3
import json
import re

# create the backend application, which only works with the database
backend_app = Flask(__name__)

# function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('../backend/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ENDPOINTS
@backend_app.route("/api", methods=["GET"])
def get_all():
    # retrieve list from the database
    # connect to DB, run the SQL statement, close the connection
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM destinations').fetchall()
    conn.close()
    # the variable rows now contains a list of sqlite Row objects,
    # which needs to be converted to a list of dictionaries (i.e. json)
    result_list = [dict(row) for row in rows]
    # now we can send it to the json library to convert it to a string
    json_output = json.dumps(result_list, indent=4)
    return(json_output), 200  # creates response json, returns HTTP response 200

# create a new destination
@backend_app.route("/api/new", methods=["POST"])
def create_dest():
    # get info from POST request
    data = request.get_json()
    dest_name = data[0].get("name")
    dest_cost = data[0].get("estimated_cost")
    dest_info = data[0].get("additional_info")

    if not dest_name or not dest_cost or not dest_info:
        return jsonify({"error": "Missing required fields"}), 400  
    
    if len(dest_name) > 20:
        return jsonify({"error": "Destination name is too long"}), 400
    
    if len(dest_info) > 100:
        return jsonify({"error": "Additional info is too long"}), 400
    
    if (not re.match(r'^[a-zA-Z0-9\s]+$', dest_name) or not re.match(r'^[a-zA-Z0-9\s]+$', dest_info)):
        return jsonify({"error": "Invalid characters"}), 400
    
    try:
        dest_cost = int(dest_cost)
        if dest_cost < 0:
            return jsonify({"error": "Estimated cost must be a positive integer"}), 400
        if dest_cost > 100000:
            return jsonify({"error": "Estimated cost is too high"}), 400
    except ValueError:
        return jsonify({"error": "Estimated cost must be an integer"}), 400

    # Connect to DB and insert information
    conn = get_db_connection()
    conn.execute('INSERT INTO destinations (name, estimated_cost, additional_info) VALUES (?, ?, ?)',
                 (dest_name, dest_cost, dest_info))
    conn.commit()
    conn.close()
    return jsonify({"name": dest_name, "cost": dest_cost, "info": dest_info}), 201  # creates response json, returns HTTP response 201


if __name__ == '__main__':
    backend_app.run(port=5001)