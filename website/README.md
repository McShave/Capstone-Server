web page for DIY home security system with user database and login functionality.

Run in a python environment with the flask framework installed (pip install flask to install it).

cd into the project directory and run 'flask --app security init-db' to initialize the database with a new user table.

Once the database is initialized, run the server with 'flask --app security run' or use 'flask --app security run --debug' to run in debug mode.

To specify the host address that the server should be listening for, use '--host' with the command. For example: flask --app security run --host="0.0.0.0"
will tell the server to listen for every IP address in the network.
