import csv
import socket
import sys
from time import sleep
import psutil
import pandas as pd
from datetime import datetime
import json

IP_ADDR = "127.0.0.1"
PORT = 12345

# Function for Datetime
def read_time():
    
    time_dict = {}
    time_dict["time"] = datetime.now().strftime("%H:%M:%S")

    return time_dict

# Function for CPU
def read_cpu_usage():
    cpu_times = psutil.cpu_times()
    cpu_stats = psutil.cpu_stats()
    cpu_freq = psutil.cpu_freq()

    cpu_dict = {}
    cpu_dict["cpu_user_time"] = cpu_times.user
    cpu_dict["cpu_idle_time"] = cpu_times.idle
    cpu_dict["cpu_interrupt_time"] = cpu_times.interrupt
    cpu_dict["cpu_utilization_percentage"] = psutil.cpu_percent()
    cpu_dict["cpu_ctx_switches"] = cpu_stats.ctx_switches
    cpu_dict["cpu_interrupts"] = cpu_stats.interrupts
    cpu_dict["cpu_soft_interrupts"] = cpu_stats.soft_interrupts
    cpu_dict["cpu_sys_calls"] = cpu_stats.syscalls
    cpu_dict["cpu_current_frequency"]= cpu_freq.current
    cpu_dict["cpu_min_frequency"]= cpu_freq.min
    cpu_dict["cpu_max_frequency"]= cpu_freq.max

    return cpu_dict

# Function for Virtual Memory
def read_virtual_memory_usage():
    memory = psutil.virtual_memory()
    memory_dict = {}

    memory_dict["total_virtual_memory"] = memory.total / (1024 ** 3) # values refer to GB
    memory_dict["available_virtual_memory"] = memory.available / (1024 ** 3) # values refer to GB
    memory_dict["virtual_memory_percentage_usage"] = memory.percent

    return memory_dict

# Function for Swap Memory
def read_swap_memory_usage():
    memory = psutil.swap_memory()
    memory_dict = {}

    memory_dict["swap_total_memory"] = memory.total / (1024 ** 3) # values refer to GB
    memory_dict["swap_available_memory"] = memory.free / (1024 ** 3) # values refer to GB
    memory_dict["swap_used_memory"] = memory.used / (1024 ** 3) # values refer to GB
    memory_dict["swap_memory_percentage_usage"] = memory.percent

    return memory_dict

# Function for Battery
def read_battery_information():
    battery = psutil.sensors_battery()
    battery_dict = {}

    battery_dict["battery_percentage"]= battery.percent
    battery_dict["power_plugged"]= battery.power_plugged
    
    return battery_dict

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

def generate_datapoint():
    dict = read_time()
    dict.update(read_cpu_usage())
    dict.update(read_virtual_memory_usage())
    dict.update(read_swap_memory_usage())
    dict.update(read_battery_information())

    return dict

# Function for Excel File (for better visualization of the dataset)
def generate_excel():
    # Load file CSV
    df_new = pd.read_csv('labelled_dataset.csv')

    # Save file in Excel format
    df_new.to_excel('labelled_dataset.xlsx', index = False)

def runtime_monitoring():
    # Create a socket object
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Bind the socket to an address and port
    sock.bind((IP_ADDR, PORT))

    # Listen for incoming connections
    sock.listen()

    # Accept a connection from the client
    connection, addr = sock.accept()
    print('Got connection from', addr)

    while True:
        dict = generate_datapoint()

        # Send the datapoint to the runtime_detector
        serialized_data = json.dumps(dict).encode('utf-8')
        connection.sendall(serialized_data)
        print(dict)
        sleep(1)
        if True:
            break

    # Close the connection
    connection.close()
    sock.close()
    sys.exit(0)
    
# Main Function
first_time = True
if __name__ == "__main__":

    # The 'try' part is excecuted for the monitoring aimed to the training of the model
    # The 'except' part is excecuted for the monitoring aimed to the anomaly detetction at runtime
    try:
        while True:
            dict = generate_datapoint()
            write_dict_to_csv("labelled_dataset.csv", dict, first_time)
            first_time = False
            print(dict)
            sleep(1)
    except KeyboardInterrupt:
        generate_excel() # Creation of the relative excel file for a better visualization of the dataset
        print("\nMonitoring aimed for the training of the model terminated!")
        print("\nRuntime monitoring starting...\n")
        runtime_monitoring() # Monitoring function aimed to anomaly detetction at runtime