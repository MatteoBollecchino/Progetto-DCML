import time

# Function that generates load on the swap memory by allocating memory beyond the RAM capacity.
def generate_swap_load(total_size_gb=4, increment_mb=100, pause_sec=1):

    block_size = increment_mb * 1024 * 1024  # Block size in bytes
    total_bytes = total_size_gb * 1024 * 1024 * 1024  # Total size in bytes

    print(f"Starting allocation of {total_size_gb} GB of memory...")
    memory = []

    try:
        for i in range(0, total_bytes, block_size):
            # Allocate memory by creating blocks of strings
            block = " " * block_size
            memory.append(block)  # Keep the block in memory
            print(f"Allocated {len(memory) * increment_mb} MB of memory.")
            time.sleep(pause_sec)  # Pause to observe the increment
    except MemoryError:
        print("Memory exhausted! RAM and swap are at their limit.")
    finally:
        print(f"Total allocated memory: {len(memory) * increment_mb} MB.")
        input("Press Enter to release the memory...")

        # Free all allocated memory
        memory.clear()

# Main function
if __name__ == "__main__":
    generate_swap_load(total_size_gb=8, increment_mb=100, pause_sec=1)
