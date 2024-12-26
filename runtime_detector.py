import csv
from time import sleep
import joblib
import socket
import json
import pandas as pd
import sys

IP_ADDR = "127.0.0.1"
PORT = 12345


def write_dict_to_csv(filename, dict_file, first_time):
    if first_time:
        file = open(filename,  'w+', newline="") 
    else:
        file = open(filename,  'a', newline="")

    writer = csv.DictWriter(file, dict_file.keys())

    if first_time:
        writer.writeheader()

    writer.writerow(dict_file)
    file.close() 

# Function for Excel File (for better visualization of the dataset)
def generate_excel():
    # Load file CSV
    df_new = pd.read_csv("runtime_result.csv")

    # Save file in Excel format
    df_new.to_excel("runtime_result.xlsx", index = False)


first_time = True
# Main Function
if __name__ == "__main__":

    # The classifier selected after training is loaded from the file
    classifier = joblib.load("classifier1.z")
    print("Selcted classifier:", classifier.__class__.__name__)

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        # Connect to the server at localhost on port 12345
        result = sock.connect_ex((IP_ADDR, PORT))
        if result == 0:
            break
        print("Connection failed")

    # With the while-instruction the runtime classifier stays reciving datapoints
    previous_dict = {}
    while True:
        # Receive data from the server
        data = sock.recv(1024)
        if data:
            received_dict = json.loads(data.decode("utf-8"))
            print("Dictionary received:", received_dict, "\n")

        # the condition is satisfied when the runtime_monitor is stopped
        if received_dict == previous_dict:
            # Close the connection
            sock.close()

            print("Runtime detection terminated!\n")
            sys.exit(0)

        previous_dict = received_dict

        # Th received dictionary is transformed in a bidimensional array
        test_dict = pd.DataFrame([received_dict])
        print(test_dict, "\n")

        # da capire come scrivere i risultati su file
        write_dict_to_csv("runtime_result.csv", received_dict, first_time)
        first_time = False
        generate_excel()

        # The model defines the label associated to the datapoint 
        predicted_label = classifier.predict(test_dict)
        print(predicted_label, "\n")

