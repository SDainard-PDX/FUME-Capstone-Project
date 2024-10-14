from printer_interface import *

JOB_FILE_DIR = './_example_jobs/'

example_printer = {
    'id' : 'A1',
    'port' : 6001,
    'apikey' : 'ABCDEFG'
}

example_job = {
    'job_id' : 1,
    'assigned_printer' : 'A1'
}

printerface = PrinterInterface()

printerface.add_printer(example_printer)

userin = ''

while example_job['job_id'] != -1:
    example_job['job_id'] = int(input("enter job ID: "))
    example_job['assigned_printer'] = str(input('enter assigned printer: '))

    while userin != 'cancel':
        print("commands:")
        print("\t start: starts the print job")
        print("\t pause: pauses the print job")
        print("\tresume: resumes the print job")
        print("\tcancel: cancels the print job")
        print("\tstatus: prints the current status of the printer")
        userin = input("run command: ")
        if userin == 'start':
            printerface.start_print_job(example_job)
        elif userin == 'pause':
            printerface.pause_print_job(example_job['assigned_printer'])
        elif userin == 'resume':
            printerface.resume_print_job(example_job['assigned_printer'])
        elif userin == 'status':
            print(printerface.get_printer_state(example_job['assigned_printer']))
        elif userin == 'cancel':
            printerface.cancel_print_job(example_job['assigned_printer'])
    

