from time import sleep
import joblib
import socket
import json
import pandas as pd
import sys

IP_ADDR = "127.0.0.1"
PORT = 12345

# Da adattare per il file txt
def write_to_txt(filename,classifier_name, dict, label, first_time):
    if first_time:
        file = open(filename,  'w+', newline="") 
        file.writelines(["Runtime Detection Results using ",classifier_name,"\n"])
    else:
        file = open(filename,  'a', newline="")

    file.writelines(["\nDatapoint:\n", str(dict), "\nPredicted label: ", str(label), "\n"])

    file.close() 


first_time = True
# Main Function
if __name__ == "__main__":

    # The classifier selected after training is loaded from the file
    classifier = joblib.load("classifier1.z")
    classifier_name = classifier.__class__.__name__
    print("Selected classifier:", classifier_name)

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

        # The received dictionary is transformed in a bidimensional array
        test_dict = pd.DataFrame([received_dict])
        print(test_dict, "\n")

        # The model defines the label associated to the datapoint 
        predicted_label = classifier.predict(test_dict)
        print(predicted_label, "\n")

        # All the information written on the terminal is also saved in a text file
        write_to_txt("runtime_result.txt",classifier_name, received_dict, predicted_label, first_time)
        first_time = False

