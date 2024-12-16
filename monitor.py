# My First Monitor
# general goal: read every second the CPU usage

import csv
import signal
import sys
from time import sleep
import psutil
import pandas as pd

# Function for CPU
def read_cpu_usage():
    cpu_t = psutil.cpu_times()
    usr_sp_cputime = cpu_t.user
    idle_time = cpu_t.idle
    cpu_dict = {"user time ": usr_sp_cputime, " idle time ": idle_time}
    cpu_dict["interrupt_time"] = cpu_t.interrupt
    return cpu_dict

# Function for Memory
def read_memory_usage():
    memory = psutil.virtual_memory()
    memory_dict = {"total memory ": memory.total, "available memory ": memory.available, "percentage usage ": memory.percent}
    return memory_dict


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
    # Carica il file CSV
    df_new = pd.read_csv('my_first_dataset.csv')

    # Salva il file in formato Excel
    df_new.to_excel('my_first_dataset.xlsx', index = False)
    
    sys.exit(0)

# Main Function
first_time = True
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler_wrapper)
    while True:
        dict = read_cpu_usage()
        dict.update(read_memory_usage())

        write_dict_to_csv("my_first_dataset.csv", dict, first_time)
        first_time = False
        print(dict)
        sleep(1)