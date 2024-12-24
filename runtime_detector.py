import subprocess
from time import sleep
import joblib
import socket

IP_ADDR = "127.0.0.1"
PORT = 12345

# Main Function
if __name__ == "__main__":

    # The classifier selected after training is loaded from the file
    classifier = joblib.load("classifier.z")
    print("Selcted classifier: %s" % (classifier.__class__.__name__))

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        # Connect to the server at localhost on port 12345
        result = s.connect_ex((IP_ADDR, PORT))
        if result == 0:
            break
        print("Connection failed")

    """
    # Il while serve a far rimanere il classifier in ascolto a runtime
    while True:
        # Receive data from the server
        data = s.recv(1024)
        print(f'Received {data.decode()}')
    """

    data = s.recv(1024)
    print(f'Received {data.decode()}')
    # Close the connection
    s.close()

    # Da usare quandoil detector riconosce un'anomaly 
    # subprocess.run('start cmd /k "echo Anomaly Detected!"', shell=True)