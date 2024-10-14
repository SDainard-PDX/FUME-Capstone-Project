from database import *
from imports import *
from requests import *
from tkinter import *

URL: str = f'http://{HOST}:{PORT}'
button_text: str = 'Send POST request test'
wolf_button_text: str = 'Send Wolf Gcode'
boat_button_text: str = 'Send boat Gcode'
crab_button_text: str = 'Send crab Gcode'
'''
s:socket = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
'''


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
            eef = post(f"{URL}/job", files=files)
    except exceptions.ConnectionError:
        print("Could not send POST request.")
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
            eef = post(f"{URL}", files=files)
    except exceptions.ConnectionError:
        print("Could not send POST request.")
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
            eef = post(f"{URL}", files=files)
    except exceptions.ConnectionError:
        print("Could not send POST request.")
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
        eef = post(f"{URL}/filament", files=files)
    except exceptions.ConnectionError:
        print("Could not add filament")
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
        eef = get(f"{URL}/job", files=files)
    except exceptions.ConnectionError:
        print("Could not add filament")
    else:
        print(f"Recieved: {eef}")


# For some reason, classname needs a space to not force lower case to the window name
window: Tk = Tk(className=" POST Sender ")

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
test_pending_button.pack()
wolf_button.pack()
boat_button.pack()
crab_button.pack()
add_filament_one.pack()
window.mainloop()
