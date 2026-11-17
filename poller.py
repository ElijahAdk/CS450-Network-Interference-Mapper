#!/usr/bin/env python3
#import random  # <test only>
import re
import socket
import subprocess
import time
from sense_hat import SenseHat

# --- Constants ---
LOGGER_NAME = "127.0.0.1"  # the Logger service's hostname in the Docker network
LOGGER_PORT = 41000      # the port that the Logger service is listening to
POLL_INTERVAL = 5.0      # the desired number of seconds between data-polling cycles
# POLL_INTERVAL is used to ensure that data is collected in a consistent, periodic manner without flooding the network with data and database PUSH requests.

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_stream:
        # Connect to the Logger service.
        data_stream.connect((LOGGER_NAME, LOGGER_PORT))

        # next_cycle tracks the target start time of the next polling cycle.
        # However, it is initialized to the current time so that data polling can begin immediately.
        next_cycle = time.monotonic()

        # This loop encompasses the polling cycles, which continue forever until the system is forcefully terminated.
        while True:
            # Get the time of the current cycle.
            curr_cycle = time.monotonic()

            # Check if it is time to perform the next polling cycle.
            if curr_cycle >= next_cycle:
                print(f"Tick at {time.strftime('%X')}")

                # --- Wi-Fi Metrics ---
                # Get the current Wi-Fi Link Quality and Signal Level metrics using the 'iwconfig' command.

                # Dummy command for testing WiFi-metrics collection in WSL on a laptop: 'netsh.exe wlan show interfaces'
                raw_iwconfig_output = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
                #raw_iwconfig_output = subprocess.run(['netsh.exe', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)  # <test only>
                #print("{", raw_iwconfig_output.stdout, "\n}", sep="")  # <debug only>

                # Extract only the desired line of output (containing Link Quality and Signal Level) from the raw 'iwconfig' output.
                desired_iwconfig_output = re.findall(r"Link Quality=[0-9]+/70 +Signal level=-?[0-9]+ dBm", raw_iwconfig_output.stdout)
                #desired_iwconfig_output = re.findall(r"Signal *: +[0-9]+%", raw_iwconfig_output.stdout)[0]  # <test only>

                # Retrieve the Link Quality and Signal Level metrics from the extracted output line. The "[::2]" slices the list of RegEx matches, returning a shallow copy containing only the even-indexed elements, which are the values we need.
                #wifi_signal_data = []
                #if (len(desired_iwconfig_output) == 0):
                    #wifi_signal_data = ["N/A", "N/A"]
                #else:
                wifi_signal_data = re.findall(r"-?[0-9]+", desired_iwconfig_output[0])[::2]
                #print("RegEx results count:", len(wifi_signal_data))
                if (len(wifi_signal_data) == 2):
                    print("Link Quality: ", wifi_signal_data[0], "/70, Signal Level: ", wifi_signal_data[1], " dBm", sep="")  # <debug only>
                #else:
                    #wifi_signal_data = ["N/A", "N/A"]
                #wifi_signal_data = [random.randint(0, 70), random.randint(-100, -30)]  # <test only>

                # --- Magnetometer Data ---
                # Retrieve the current magnetic field readings from the on-board magnetometer

                # Initialize an object to represent the host Sense HAT Raspberry Pi.
                sensehat = SenseHat()

                # Get the X-, Y-, and Z-axis magnetometer readings.
                raw_magnet_data = sensehat.get_compass_raw()
                magnet_x = raw_magnet_data['x']
                magnet_y = raw_magnet_data['y']
                magnet_z = raw_magnet_data['z']
                print(f"Magnetometer readings: (X: {magnet_x:.6f} µT | Y: {magnet_y:.6f} µT | Z: {magnet_z:.6f} µT)")
                #magnet_x = random.uniform(-10, 10)  # <test only>
                #magnet_y = random.uniform(-10, 10)  # <test only>
                #magnet_z = random.uniform(-10, 10)  # <test only>

                # --- Data Output ---
                # Send the retrieved data to the Logger service.

                data_string = f"{wifi_signal_data[0]} {wifi_signal_data[1]} {magnet_x:.6f} {magnet_y:.6f} {magnet_z:.6f}"
                #data_string = f"62 -46 0.356254 -1.595278 0.004625\n"  # <test only>
                data_stream.sendall(data_string.encode('utf-8'))

                # Schedule the next poll cycle based on the current cycle's target
                next_cycle += POLL_INTERVAL
            # End of the poll-cycle code.

            # Calculate how long we still need to wait before beginning the next poll cycle.
            sleep_time = next_cycle - time.monotonic()

            # Sleep until the next poll cycle's target time. If sleep_time is zero, then we are right on time for the next cycle and do not need to wait. If sleep_time is negative, then we need to start the next cycle immediately to catch up.
            if sleep_time > 0:
                time.sleep(sleep_time)
if __name__ == "__main__":
    main()
