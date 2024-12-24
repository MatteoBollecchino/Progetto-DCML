from tqdm import tqdm
from time import sleep
import psutil

# Main function
if __name__ == "__main__":

    with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
        while True:
            cpubar.n=psutil.cpu_percent()
            rambar.n=psutil.virtual_memory().percent
            cpubar.refresh()
            rambar.refresh()
            sleep(1)