# Author(s): Tazwell Borquist

import octorest
from printer_interface.fume import FilamentMultiplexer

DEBUG = False

PrinterId = str

PRINTER_URL = 'http://localhost'
JOB_FILE_DIR = "./jobs/" # UPDATE LATER

# The printer interface a composition of the 
class PrinterInterface:
    job_file_path = '.'

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PrinterInterface, cls).__new__(cls)
        return cls.instance

    def __init__(self, printer_config=None):
        self.octo_instance : dict[PrinterId, octorest.OctoRest] = dict()
        self.printer_states : dict = dict()

        self.fume : FilamentMultiplexer = FilamentMultiplexer(
            # Filament Multiplexer Initialization Args
        )

        self.printer_mutex : list = list() # Unsure if we'll need this

        self.post_job_action : dict[PrinterId, str] = dict() # was an event queue, but this makes more sense

        if isinstance(printer_config, dict):
            for printer in printer_config["printers"]: # printer_config["printers"] : list[dict]
                self.add_printer(printer)

        if DEBUG:
            print("Hello from PrinterInterface()__init__()!")
        # return # __init__()

    def _printer_exists(self, printer: PrinterId):
        if not isinstance(printer, PrinterId):
            raise ValueError("printer key is not correct type")
        if printer in self.octo_instance:
            return True
        return False

    def add_printer(self, options: dict) -> bool:
        """ Adds a printer to the self.octo_instance variable.
        Accessible with: self.octo_instance[PrinterId]
        """
        if not isinstance(options, dict):
            raise ValueError("PrinterInterface.add_printer() requires 'options' to be a dict")

        if DEBUG:
            print(options)

        REQ_ITEMS = ['id', 'port', 'apiKey']
        for req in REQ_ITEMS:
            if not req in options:
                raise ValueError(f"PrinterInterface.add_printer() requires '{req}' to be a key of 'options'")

        if DEBUG:
            print("PrinterInterface().add_printer(): adding", options["id"])

        try:
            self.octo_instance[options['id']] = octorest.OctoRest(
                url=PRINTER_URL + ':' + str(options['port']),
                apikey=options['apiKey'] )
            self._force_update_printer_sate(options['id'])
        except Exception as e:
            print(f"Failed to connect to printer {options['id']}")
            print(e)
            return False
        return True
        

    def is_printer_ready(self, printer : PrinterId) -> bool:
        """ Returns True if requested printer is available to start a print job 
        """
        if not self._printer_exists(printer):
            return False
        state = self.get_printer_state(printer)
        if state != "ReadyToPrint":
            return False
        return True


    def start_print_job(self, printer : PrinterId, print_job) -> bool:
        """
        Args:
            printer: id of the printer to start, appears in job queue as 'printer_assignment'
            print_job: dictionary of the queued print job

        Returns:
            False: if the printer is busy, or the print fails to upload/start
            True: if the file was sucessfully uploaded and started

        Raises:
            ValueError: if an arg of an incorrect type has been passed
        """
        if not self._printer_exists(printer):
            return False
        if not isinstance(print_job, dict):
            raise ValueError("print_job arg is not a dict")

        if not self.is_printer_ready(printer):
            return False

        try:
            self.octo_instance[printer].upload(
                file  = JOB_FILE_DIR + print_job["job_name"],
                print = True )
        except RuntimeError as e:
            # OctoRest.upload() raises RuntimeError if printer returns a status code other than: '20x is-OK'
            print(e)
            return False
        self.printer_states[printer] = "Printing"
        return True


    def make_printer_ready(self, printer : PrinterId):
        if not self._printer_exists(printer):
            return False
        self.printer_states[printer] = "ReadyToPrint"

    def pause_print_job(self, printer : PrinterId) -> bool:
        if not self._printer_exists(printer):
            return False
        try:
            self.octo_instance[printer].pause_command('pause')
        except RuntimeError as e:
            # OctoRest.pause() raises RuntimeError if printer returns a status code other than: '20x is-OK'
            print(e)
            return False
        return True

    def resume_print_job(self, printer : PrinterId) -> bool:
        if not self._printer_exists(printer):
            return False
        try:
            self.octo_instance[printer].pause_command('resume')
        except RuntimeError as e:
            # OctoRest.resume() raises RuntimeError if printer returns a status code other than: '20x is-OK'
            print(e)
            return False
        return True


    def cancel_print_job(self, printer : PrinterId) -> bool:
        if not self._printer_exists(printer):
            return False
        try:
            self.octo_instance[printer].cancel()
        except RuntimeError as e:
            # OctoRest.cancel() raises RuntimeError if printer returns a status code other than: '20x is-OK'
            print("PrinterInterface.cancel_print_job() failed to cancel print")
            print(e)
            return False
        return True


    def send_gcode(self, printer : PrinterId, gcode : str) -> bool:
        if not self._printer_exists(printer):
            return False
        try:
            self.octo_instance[printer].gcode(gcode)
        except RuntimeError as e:
            # OctoRest.resume() raises RuntimeError if printer returns a status code other than: '20x is-OK'
            print(e)
            return False
        return True

    def get_client(self, printer : PrinterId) -> octorest.OctoRest | None:
        """ Returns an OctoRest client of the requested printer.
        """
        if not self._printer_exists(printer):
            return False
        if not printer in self.octo_instance:
            return None
        return self.octo_instance[printer]

    '''

    def get_printer_id(self, filament : FilamentId) -> PrinterId:
        """ Returns the PrinterId of the printer filament is currently sent to.
        """
        if not isinstance(filament, FilamentId):
            raise ValueError()


    def is_filament_in_printer(self, printer : PrinterId, filament : FilamentId) -> bool:
        """ Checks if filament is currently in printer.
        """
        if not isinstance(printer, PrinterId) or  not isinstance(filament, FilamentId):
            raise ValueError()
        return None


    def send_filament_to_printer(self, printer : PrinterId, filament : FilamentId) -> bool:
        """ Attempts to send filament to printer.
        Returns: True on success (will require human intervention), 
                 False if requested operation is not possible 
        """
        if not isinstance(printer, PrinterId) or  not isinstance(filament, FilamentId):
            raise ValueError()
        return None
    '''

    def _force_update_printer_sate(self, printer) -> bool:
        if not self._printer_exists(printer):
            return False
        try:
            self.printer_states[printer] = self.octo_instance[printer].state()
        except Exception as e:
            print(e)
            return False
        return True
    
    def get_printer_state(self, printer) -> str:
        """ Returns current state of printer(s).
        Args: PrinterId(s) of the printer states requested.
        Returns: The current state of the printers requested, if no specific 
                printer is requested, returns the states of all printers.
         """
        if not self._printer_exists(printer):
            return None
        return self.printer_states[printer]

    def update(self) -> None:
        # I don't know what this'll do
        pass
