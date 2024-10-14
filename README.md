# CS FUME Capstone

# Breif Project Description 
The FUME project serves as an intermediary between the EPL PARQE system and the ME FUME project, 
automating the management and routing of 3D printing jobs within the Electronics Prototyping Lab. It 
optimizes printer utilization, reduces manual intervention, and provides real-time monitoring and 
reporting.

# More Documentaion
This README contains just the basics you need to get it up and running. For a high-level overview, 
check out the [Project Document](Project_document.pdf). If you want to see more of the developer design decisions, see the 
[Dev Document](#).


# Setup & Run in EPL

In a Linux or Mac environment, run the following script to get the 
application and database running:

```
./setup.sh
```

This will start up the PostgreSQL database in a Docker container, the backend Flask application, and the frontend Flask application, each on dynamically assigned ports.

Once the script is done running, click on the first server url. It will bring up the Flask 
application.

If the OctoPrint instances are connected on either the test bench or the computer up front, and if there is a printer that matches a job, you should see it start printing.


# Setup & Run Locally
Follow the same process as running in EPL. If you don't have a connected OctoPrint instance, you can still see the database and graphical interface, but it won't print any jobs.


# Sending Test Orders / Simulating PARQE

Run send.py on its own, set the port to whatever FUME is using to receive orders, and click one of the buttons to send a test order.