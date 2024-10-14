'''
Important note: If working with a string of text uart.write() will 
raise an error if the argument is a string. To get around this with
unformatted strings you can simply add a 'b' to the start I.E.

    "hello world!\n" --> b"hello world!\n"

This also works for single/triple quote strings.

For formatted strings you need to use .encode('ascii') I.E.

    f"hello {name}\n" --> f"hello {name}\n".encode('ascii')

        OR

    "hello {}".format(name) --> "hello {}".format(name).encode('ascii')


This is because the uart.write() method only takes a bytes or bytearray
object, and the default encoding for strings in python is 'utf-8', which 
should honestly be compatible, but isn't. :/

'''

NUM_FILAMENT_SPOOLS = 4 # the maximum number of filament spools the machine supports
NUM_PRINTER_TRACKS = 4 # the maximum number of printers the machine can route to

def echo(**kwargs):
    uart.write(bytes.join(b' ', kwargs['fullcomm']))

def info(filament, printer, **__):
    # uart.write() current state of machine
    uart.write(b'info function\n')

# EXTRA COMMANDS GO HERE

'''
                HOW TO CREATE A NEW COMMAND:

Step 1: Define the new function:

def my_new_command():
    pass

Step 2: Give it arguments based on what inputs it should take.
        For this function it will take a filament number and a
        printer (track) number.

        The three arguments already included are 'filament',
        'printer', and 'distance'.

def my_new_command(filament, printer):
    pass

Step 3: Put **__ as the last argument. This will 'catch' any
        extra arguments passed to the function. The name can
        be **anything, but if it is '__' it will simply ignore
        the argument.

def my_new_command(filament, printer, **__):
    pass

Step 4 (optional): If you want to be able to send serial communications
                   back to the connected machine: use uart.write(msg)
                   to send the message.



Step 5: Write your command. Note that it is important to check if any
        argument is outside of an allowed range of values.

def my_new_command(filament, printer, **__):
    global uart
    # do something
    uart.write(b'my_new_command did something!')

Step 6: Once your new command has been created you need to 'register'
        it by adding it to the 'funcs' dictionary below. This is where
        you decide what the command should be called by from the serial
        communication. The key is the command, while the value is the
        name of the function itself.

        In this case the new command would be accessable by the serial
        connection with the template: b'new F# P#'
'''

funcs = {
    # registering my_new_command:
    # b'new' : my_new_command,

    # sample command registrations:
    #b'extend'  : extend_fil,
    #b'retract' : retract_fil,
    #b'route'   : route_fil_to_printer,

    b'echo' : echo,
    b'info' : info
}

#
# Unless you want to add another arg that a function could take you shouldn't
# have to touch handle_command or get_int_with_prefix hopefully. 
#

def get_int_with_prefix(args, prefix):
    for arg in args:
        if isinstance(arg, bytes) and arg.startswith(prefix) and arg.lstrip(prefix).isdigit():
            return int(arg.lstrip(prefix))
    return -1

def handle_command():
    global uart, funcs
    if uart.any() > 0:
        comm = uart.readline()
        comm = comm.strip(b'\n').split(b' ')
        if not comm[0] in funcs: # don't procceed if command does not exist
            return 
        cargs = dict()
        cargs['filament'] = get_int_with_prefix(comm, b'F')
        cargs['printer']  = get_int_with_prefix(comm, b'P')
        cargs['distance'] = get_int_with_prefix(comm, b'D')
        cargs['fullcomm'] = comm
        # call funcs[comm[0]] with args: filament=some_int, printer=some_int, and distance=some_int
        funcs[comm[0]](**cargs) 
        # NOTE: the function called MUST check if the arguments passed are valid or not



from machine import UART

uart = UART(1, 9600) # 9600 baudrate default

while True:
    handle_command()
    # MAINLOOP