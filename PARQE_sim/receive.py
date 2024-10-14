from imports import *
from flask import Flask, request
#from http import HTTPStatus
from database.database import Connection
from datetime import date, time, datetime
from os import mkdir
#from requests import post
from send import DEST

MAX_ATTEMPTS:int = 3

'''
Recieves orders and breaks them up into jobs
to be sent to the database
'''
server = Flask(__name__)
@server.route('/order', methods=['POST'])
def make_jobs_from_order():
    with Connection() as conn:
        info:dict = loads(request['json'])
        current_time:str = datetime.now().strftime('%H%M%S')
        job_name:str = str(request.files['file'].name + current_time)
        for x in range(int(info['order_quantity'])):
            conn.add_job(
                info['order_id'], 
                info['order_quantity'],
                job_name, -1,
                info['nozzle_size'],
                info['filament_type'],
                info['filament_color'],
                str(request.files['file'].stream.read())
                )