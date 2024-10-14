from flask import Flask, request, render_template, redirect, flash
import json

from Web_UI.JSON_functions.updateJSON import addPrinter
from DB_and_comm.database.database import Connection
from printer_interface.printer_interface import PrinterInterface

app = Flask(__name__)
app.secret_key = "secret"

with open("./Web_UI/data/printers.json", "r") as jsonFile:
    printer_data = json.load(jsonFile)
    for printer in printer_data["printers"]:
        PrinterInterface().add_printer(printer)

#FUNC: Ensures we have a landing page by redirecting when opening app
@app.route('/')
def home():
    return redirect('/printer_status')


#FUNC: Quick check display of printer status' & jobs w/ issues
@app.route('/printer_status')
def status():
    # with closes the file
    with open('./Web_UI/data/jobs.json') as jobs_file, \
            open('./Web_UI/data/printers.json') as printer_file:
        return render_template("printer_status.html",
                               jobs=json.load(jobs_file),
                               printers=json.load(printer_file))


#FUNC: Display current printers w/ setting and filament options
@app.route('/printer_page', methods=["GET"])
def page():
    with open('./Web_UI/data/printers.json') as printer_file, \
            open('./Web_UI/data/filaments.json') as filament_file:
        return render_template("printer_page.html",
                               printers=json.load(printer_file),
                               filaments=json.load(filament_file))


#FUNC: [Get] info for added printer -> [POST] add the printer & redirect
@app.route('/add_printer', methods=["GET", "POST"])
def add_printer():
    if request.method == "POST":
        printerID = request.form.get("printer-id")
        printerPort = int(request.form.get("printer-port"))
        printerAPI = request.form.get("printer-api")
        filamentID = request.form.get("filament-id")
        nozzleSize = request.form.get("nozzle-size")
        ret = addPrinter(printerID, printerPort, printerAPI, filamentID, nozzleSize)
        connection: Connection = Connection() #TODO figure out filament id issue
        connection.add_printer(printerID, filamentID, "no color", printerPort, printerAPI)
        if ret:
            flash("Printer " + printerID + " Added")
        else:
            flash("Error printer NOT added!")
        return redirect('printer_page')

    with open('./Web_UI/data/data.json') as settings_file:
        return render_template("add_printer.html", settings=json.load(settings_file))


@app.route('/configure_printer', methods=["GET", "POST"])  #TODO - set up like add filament and printer
def configure():
    with open('./Web_UI/data/data.json') as settings_file, \
            open('./Web_UI/data/printers.json') as printer_file:
        return render_template("configure_printer.html",
                               settings=json.load(settings_file),
                               printers=json.load(printer_file))


#FUNCE: [Get] info for added filament-> [POST] add the filament & redirect
@app.route('/add_filament', methods=["GET", "POST"])
def add_filament():
    if request.method == "POST":
        filamentColor = request.form.get("filament-color")
        filamentType = request.form.get("filament-type")
        filamentMaker = request.form.get("filament-manufacturer")
        connection: Connection = Connection()
        ret = connection.add_filament(filamentType, filamentColor, filamentMaker)
        if ret:
            flash("Filament " + filamentColor + " Added")
        else:
            flash("Error filament NOT added!")
        return redirect('/printer_page')

    with open('./Web_UI/data/data.json') as settings_file:
        return render_template("add_filament.html", settings=json.load(settings_file))


# TODO - IS settings better as data so that in the html it's data.settings.XXX?


#FUNC: Display all jobs in the queue w their information
@app.route('/job_queue')
def queue():
    with open('./Web_UI/data/jobs.json') as jobs_file:
        return render_template("job_queue.html", jobs=json.load(jobs_file))


#FUNC: Provide a page to change the apps settings
@app.route('/app_settings')
def settings():
    return redirect('/printer_status')
    # MAKE PAGE TO SHOW VALUES AND MAKE CHANGES
    # Use JSON_functions to update data.app-settings values

'''
TODO
- Recieves orders and breaks them up into jobs to be sent to the database
- Create folders named after today's date (if not exists)
- Rename gcode file to [order number].gcode and store in today's directory

NOTICE
Most of this function serves to prevent syntax errors and is not currently functional
'''
#FUNC: Receives orders from PARQE, breaks them up into jobs, stores jobs in database
server = Flask(__name__)
@server.route('/order', methods=['POST'])
def make_jobs_from_order():
    with Connection() as conn:
        info:dict = json.loads(request['json'])
        '''
        current_time:str = datetime.now().strftime('%H%M%S')
        job_name:str = str(request.files['file'].name + current_time)
        '''
        job_name:str = str(info['job_number'] + '.gcode')
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

@app.route('/stop')
def stop():
    printerID = request.form.get('printerid')
    pint = PrinterInterface()
    pint.cancel_print_job(printerID)

if __name__ == '_mma bring loga_main__':
    app.run()
