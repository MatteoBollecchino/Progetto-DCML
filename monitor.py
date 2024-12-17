import csv
import signal
import sys
from time import sleep
import psutil
import pandas as pd

# Function for CPU
def read_cpu_usage():
    cpu_t = psutil.cpu_times()
    cpu_dict = {}
    cpu_dict["cpu_user_time"] = cpu_t.user
    cpu_dict["cpu_idle_time"] = cpu_t.idle
    cpu_dict["cpu_interrupt_time"] = cpu_t.interrupt
    cpu_dict["cpu_utilization_percentage"] = psutil.cpu_percent()
    cpu_dict["cpu_frequency"]= psutil.cpu_freq()
    return cpu_dict

# Function for Memory
def read_memory_usage():
    memory = psutil.virtual_memory()
    memory_dict = {}
    memory_dict["total_memory"] = memory.total / (1024 ** 3) # values refer to GB
    memory_dict["available_memory"] = memory.available / (1024 ** 3) # values refer to GB
    memory_dict["memory_percentage_usage"] = memory.percent
    return memory_dict

# Function for Battery
def read_battery_information():
    battery = psutil.sensors_battery()
    battery_dict = {}
    battery_dict["battery_percentage"]= battery.percent
    battery_dict["power_plugged"]= battery.power_plugged
    return battery_dict

# Function for Excel File
def write_dict_to_csv(filename, dict_file, first_time):
    if first_time:
        f = open(filename,  'w+', newline="") 
    else:
        f = open(filename,  'a', newline="")

    w = csv.DictWriter(f,dict_file.keys())

    if first_time:
        w.writeheader()

    w.writerow(dict_file)
    f.close()

def signal_handler_wrapper(signum, frame):
    signal_handler()

def signal_handler():
    # Load file CSV
    df_new = pd.read_csv('labelled_dataset.csv')

    # Save file in Excel format
    df_new.to_excel('labelled_dataset.xlsx', index = False)
    
    sys.exit(0)

# Main Function
first_time = True
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler_wrapper)
    while True:
        dict = read_cpu_usage()
        dict.update(read_memory_usage())
        dict.update(read_battery_information())

        write_dict_to_csv("labelled_dataset.csv", dict, first_time)
        first_time = False
        print(dict)
        sleep(0.5)