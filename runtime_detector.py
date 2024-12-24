import subprocess
from time import sleep
import joblib
import socket
import json
import sklearn

IP_ADDR = "127.0.0.1"
PORT = 12345

# Main Function
if __name__ == "__main__":

    # The classifier selected after training is loaded from the file
    classifier = joblib.load("classifier.z")
    print("Selcted classifier: %s" % (classifier.__class__.__name__))

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        # Connect to the server at localhost on port 12345
        result = sock.connect_ex((IP_ADDR, PORT))
        if result == 0:
            break
        print("Connection failed")

    # With the while-instruction the runtime classifier stays reciving datapoints
    while True:
        # Receive data from the server
        data = sock.recv(1024)
        if data:
            received_dict = json.loads(data.decode('utf-8'))
            print(f"Dizionario ricevuto: {received_dict}")

        # Trasforma 'dict' in un array bidimensionale
        # Capire come è strutturato il parametro di predict in anomaly_detector 

        break

        """
        predicted_label = classifier.predict([[received_dict]])

        if predicted_label == "anomaly":
            subprocess.run('start cmd /k "echo Anomaly Detected!"', shell=True)
            break
        """

    # Close the connection
    sock.close()

    # Da usare quandoil detector riconosce un'anomaly 
    # subprocess.run('start cmd /k "echo Anomaly Detected!"', shell=True)