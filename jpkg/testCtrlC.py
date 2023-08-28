import signal
import time

# Define a function to handle Ctrl+C
def ctrl_c_handler(signum, frame):
    print("Ctrl+C was pressed, but I won't exit!")
    # You can put your custom code here to handle the Ctrl+C event gracefully

# Set the custom handler for the SIGINT signal (Ctrl+C)
signal.signal(signal.SIGINT, ctrl_c_handler)

try:
    print("Running... Press Ctrl+C to test.")
    while True:
        # Your main script logic goes here
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting gracefully")
