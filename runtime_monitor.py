import socket
import sys
from time import sleep
import psutil
import json

IP_ADDR = "127.0.0.1"
PORT = 12345

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

    return cpu_dict

# Function for virtual memory
def read_virtual_memory_usage():
    memory = psutil.virtual_memory()
    memory_dict = {}

    memory_dict["available_virtual_memory"] = memory.available / (1024 ** 3) # values refer to GB
    memory_dict["virtual_memory_percentage_usage"] = memory.percent

    return memory_dict

# Function for swap memory
def read_swap_memory_usage():
    memory = psutil.swap_memory()
    memory_dict = {}

    memory_dict["swap_available_memory"] = memory.free / (1024 ** 3) # values refer to GB
    memory_dict["swap_used_memory"] = memory.used / (1024 ** 3) # values refer to GB
    memory_dict["swap_memory_percentage_usage"] = memory.percent

    return memory_dict

# Function for battery
def read_battery_information():
    battery = psutil.sensors_battery()
    battery_dict = {}

    battery_dict["battery_percentage"]= battery.percent
    battery_dict["power_plugged"]= battery.power_plugged
    
    return battery_dict 

# Function for the generation of a datapoint, to be analyzed from the runtime_detector
def generate_datapoint():
    dict = read_cpu_usage()
    dict.update(read_virtual_memory_usage())
    dict.update(read_swap_memory_usage())
    dict.update(read_battery_information())

    return dict

# Function to monitor the system and send the datapoints to the runtime_detector
def runtime_monitoring():
    # Create a socket object
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Bind the socket to an address and a port
    sock.bind((IP_ADDR, PORT))

    # Listen for the incoming connection of the runtime_detector
    sock.listen()

    # Accept the connection from the runtime_detector
    connection, addr = sock.accept()
    print("Got connection from", addr, "\n")

    try:
        while True:
            dict = generate_datapoint()

            # Send the datapoint to the runtime_detector
            serialized_data = json.dumps(dict).encode('utf-8')
            connection.sendall(serialized_data)
            print(dict, "\n")
            sleep(1)
    except KeyboardInterrupt:
        # Close the connection
        connection.close()
        sock.close()
        print("Runtime monitoring terminated!\n")
        sys.exit(0)
    
# Main Function
if __name__ == "__main__":
    print("\nRuntime monitoring starting...\n")

    # Monitoring function aimed to anomaly detetction at runtime
    runtime_monitoring() 
