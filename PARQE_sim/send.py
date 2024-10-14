import sys, os
# Enable access to modules in parent folder (Might be a Windows thing?)
sys.path.append(f'{os.path.dirname(__file__)}/..')

from database.database import *
from imports import *
from requests import *
from tkinter import *

# init port with default value (5000)
port:str = str(PORT)
# init default destination
dest: str = f'http://{HOST}:{port}'
port_entry_label: str = 'FUME port:'
button_text: str = 'Send POST request test'
wolf_button_text: str = 'Send Wolf Gcode'
boat_button_text: str = 'Send boat Gcode'
crab_button_text: str = 'Send crab Gcode'

# Basic function for handling POST errors
def handle_connection_error(response) -> None:
    if response:
        print('Could not connect to FUME')

# This function uses *args to hold items from 
# Callbacks I am not using
def set_targ(new_port:str) -> None:
    global port 
    global dest 
    port = new_port
    dest = f'http://{HOST}:{port}'

def send_order(data:dict) -> Response:
    return post(f"{dest}/order", files=data)

def send_wolf():
    #Making dummy JSON, since we don't know how it will be structured
    json_dictionary = {
        "order_id": "1",
        "job_name": "Christians Job",
        "printer_assignment": 1,
        "quantity": 1,
        "nozzle_size": "4",
        "filament_type": "pla",
        "filament_color": "red"
    }
    json_data = dumps(json_dictionary, default=str)
    try:

        #Opens gcode and file location specified
        with open(f"example_gcodes/wolf.gcode", 'rb') as file:

            # Create dictionary with json data and raw gcode file
            files = {
                'json': json_data,
                'file': file
            }
            eef = send_order(files)
    except exceptions.ConnectionError as e:
        handle_connection_error(e)
    else:
        print(f'Received "{eef}"')


def send_boat():
    json_dictionary = {
        "order_id": "2",
        "order_quantity": "1",
        "nozzle_size": "4",
        "filament_type": "PLA",
        "filament_color": "orange"
    }
    json_data = dumps(json_dictionary, default=str)
    try:
        with open(f"example_gcodes/boat_bench.gcode", 'rb') as file:
            # Create dictionary with json data and raw gcode file
            files = {
                'json': json_data,
                'file': file
            }
            eef = send_order(files)
    except exceptions.ConnectionError as e:
        handle_connection_error(e)
    else:
        print(f'Received "{eef}"')


def send_crab():
    json_dictionary = {
        "order_id": "3",
        "order_quantity": "2",
        "nozzle_size": "6",
        "filament_type": "PLA",
        "filament_color": "red"
    }
    json_data = dumps(json_dictionary, default=str)

    try:
        with open(f"example_gcodes/mud_crab.gcode", 'rb') as file:
            # Create dictionary with json data and raw gcode file
            files = {
                'json': json_data,
                'file': file
            }
            eef = send_order(files)
    except exceptions.ConnectionError as e:
        handle_connection_error(e)
    else:
        print(f'Received "{eef}"')


def add_red_osun():
    json_dict = {
        "filament_type": "pla",
        "filament_color": "red",
        "manufacturer": "osun"
    }
    json_data = dumps(json_dict, default=str)
    files = {
        'json': json_data
    }
    try:
        eef = post(f"{dest}/filament", files=files)
    except exceptions.ConnectionError as e:
        handle_connection_error(e)
    else:
        print(f"Recieved: {eef}")


def test_get_pending():
    json_dict = {
        "job_status": "PENDING",
    }
    json_data = dumps(json_dict, default=str)
    files = {
        'json': json_data
    }
    try:
        eef = get(f"{dest}/order", files=files)
    except exceptions.ConnectionError as e:
        handle_connection_error(e)
    else:
        print(f"Recieved: {eef}")

def print_port():
    print(port)


# For some reason, classname needs a space to not force lower case to the window name
window: Tk = Tk(className=" POST Sender ")

port_frame:Frame = Frame(window)

target_label: Label = Label(
    port_frame,
    text=port_entry_label
)
target_label.pack(side=LEFT)

# Guts of target_port
port_var:StringVar = StringVar(value=port)
# call set_targ when value updated
# n, i, and o are captures for variables I'm not using
port_var.trace_add('write', lambda n, i, o: set_targ(port_var.get()))

target_port: Entry = Entry(
    port_frame,
    textvariable=port_var
)
target_port.pack(side=RIGHT)

port_check_button:Button = Button(
    window,
    text='Check Port',
    command=print_port,
    font=('comic sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

test_pending_button: Button = Button(
    window,
    text="Test pending",
    command=test_get_pending,
    font=('Comic Sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

wolf_button: Button = Button(
    window,
    text=wolf_button_text,
    command=send_wolf,
    font=('Comic Sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

boat_button: Button = Button(
    window,
    text=boat_button_text,
    command=send_boat,
    font=('Comic Sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

crab_button: Button = Button(
    window,
    text=crab_button_text,
    command=send_crab,
    font=('Comic Sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

add_filament_one: Button = Button(
    window,
    text="Add red pla from oSun",
    command=add_red_osun,
    font=('Comic Sans', 30),
    fg='purple',
    bg='black',
    activeforeground='purple',
    activebackground='black'
)

# target_label.pack()
# target_port.pack()

port_frame.pack()
port_check_button.pack()
wolf_button.pack()
boat_button.pack()
crab_button.pack()
add_filament_one.pack()

window.mainloop()
