import json
from printer_interface.printer_interface import PrinterInterface
from DB_and_comm.database.database import Connection

pint = PrinterInterface()

def addPrinter(printerID, printerPort, printerAPI, filamentType, nozzleSize):
    try:
        with open('./Web_UI/data/printers.json', 'r') as jsonFile:
            printer_data = json.load(jsonFile)
            jsonFile.close()
        added_printer = {
            "id": printerID, 
            "port": printerPort,
            "apikey": printerAPI,
            "filamentType": filamentType,
            "nozzleDiameter": nozzleSize,
            "jobStatus": "Ready"
            }
        with open('./Web_UI/data/printers.json', 'w') as jsonFile:
            printer_data["printers"].append(added_printer)
            json.dump(printer_data, jsonFile, indent=4)
            jsonFile.close()
        #add_printer(printerID, filamentID, printerPort, printerAPI)
        pint.add_printer(added_printer)
        return 1
    except:
        return 0
    
    '''
    def updateJSON():
    with open('./data/printers.json', "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()

    #do work here

    with open('./data/printers.json', "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)
        jsonFile.close()
    '''