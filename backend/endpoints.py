
from db_and_request_demo.imports import *
from flask import Flask, request, Response, jsonify
from sqlalchemy import Connection
from database.database import *

server = Flask(__name__)


@server.route('/filament', methods=['POST'])
def add_filament():
    """
    Adds a new filament to the database
    Json should be formatted as follows:

    {
        "filament_type":"pla",
        "filament_color":"dark blue",
        "manufacturer":"eSun"
    }
    :return:
    """
    connection: Connection = Connection()
    json_str = request.files['json'].read().decode('utf-8')
    loaded_json = loads(json_str)
    filament_type = loaded_json["filament_type"]
    filament_color = loaded_json["filament_color"]
    manufacturer = loaded_json["manufacturer"]

    ret_val = connection.add_filament(filament_type, filament_color, manufacturer)
    if ret_val is not None:
        return Response(status=200)
    return Response(status=400)


@server.route('/job', methods=['POST'])
def add_job():
    """
    Adds a new job
    Json should be formatted as follows:
    {
        "order_id":"1",
        "job_name":"example job name",
        "printer_assignment":"1",
        "quantity": 1
        "nozzle_size":4,
        "filament_type":"pla+",
        "filament_color":"dark blue"
    }
    This request should also contain a file being the raw GCode
    :return:
    """
    connection: Connection = Connection()

    json_str = request.files['json'].read().decode('utf-8')
    loaded_json = loads(json_str)
    gcode = str(request.files["file"].stream.read())
    order_id = int(loaded_json["order_id"])
    quantity = int(loaded_json["quantity"])
    job_name = loaded_json["job_name"]
    printer_assignment = int(loaded_json["printer_assignment"])
    nozzle_size = int(loaded_json["nozzle_size"])
    filament_type = loaded_json["filament_type"]
    filament_color = loaded_json["filament_color"]
    ret_val = connection.add_job(order_id, quantity, job_name, printer_assignment, nozzle_size, filament_type, filament_color,
                                 file_text=gcode)
    if ret_val is not None:
        return Response(status=200)
    return Response(status=400)


@server.route('/job', methods=['PUT'])
def update_job():
    """
    Updates a job status in the database
        Json should be formatted as:
        {
            "job_status":"COMPLETE"
            "order_id":245
        }
    """
    connection: Connection = Connection()
    json_str = request.files['json'].read().decode('utf-8')
    loaded_json = loads(json_str)
    status = loaded_json["job_status"]
    order_id = loaded_json["order_id"]
    ret_val = connection.update_job_status(order_id, status)
    if ret_val is not None:
        return Response(status=200)
    return Response(status=400)


@server.route('/printer', methods=['POST'])
def add_printer():
    """
    Adds a new printer to the database
    Json should be formatted as follows
    {
    TODO: Figure out information required for adding a printer
    :return:
    """


@server.route('/job', methods=['GET'])
def get_pending_jobs():
    """
    Retrieves all jobs with job_status PENDING
    """
    connection: Connection = Connection()
    json_str = request.files['json'].read().decode('utf-8')
    loaded_json = loads(json_str)
    status = loaded_json["job_status"]
    result = connection.get_all_jobs_from_status(status)
    return jsonify(result)


'''
# Variable declaration
running:bool = True
clients:list = list(socket)

# Function definitions
def listen_for_new_connections():
    while running:
        # listen for new connections and add them to the client list
        pass
    # close all client connections

# MAIN
shepard = Thread(listen_for_new_connections)

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
'''
