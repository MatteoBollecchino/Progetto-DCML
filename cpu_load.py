import multiprocessing
import time

# Function that simulates heavy CPU load performing infinite calculations to keep the core busy.
def intensive_work():
    
    while True:
        _ = sum(i * i for i in range(10**1))  # Intensive calculation

# Function that starts multiple processes to generate significant CPU load.
def generate_cpu_load(num_processes=None):
    
    # num_processes = None -> All the cores are used
    if num_processes is None:
        num_processes = multiprocessing.cpu_count() - 1  # High number of cores

    print("Generating CPU load on", num_processes, "cores...")
    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=intensive_work)
        process.start()
        processes.append(process)
    
    try:
        # Keep the program running to observe CPU usage
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupt received. Stopping processes...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()

# Main function
if __name__ == "__main__":
    generate_cpu_load()
