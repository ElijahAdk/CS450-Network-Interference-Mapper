import re
import socket
import subprocess
from sense_hat import SenseHat

# --- Constants ---
LOGGER_IP = "127.0.0.1"  # the Logger service's hostname in the Docker network
LOGGER_PORT = 41000      # the port that the Logger service is listening to

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_stream:
    # Connect to the Logger service.
    data_stream.connect((LOGGER_IP, LOGGER_PORT))

    # --- Wi-Fi Metrics ---
    # Get the current Wi-Fi Link Quality and Signal Level metrics using the 'iwconfig' command.

    # Dummy command for testing WiFi-metrics collection in WSL on a laptop: 'netsh.exe wlan show interfaces'
    raw_iwconfig_output = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
    #raw_iwconfig_output = subprocess.run(['netsh.exe', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    print("{", raw_iwconfig_output.stdout, "\n}", sep="")

    # Extract only the desired line of output (containing Link Quality and Signal Level) from the raw 'iwconfig' output.
    desired_iwconfig_output = re.findall(r"Link Quality=[0-9]+/70 +Signal level=-?[0-9]+ dBm", raw_iwconfig_output.stdout)
    #desired_iwconfig_output = re.findall(r"Signal *: +[0-9]+%", raw_iwconfig_output.stdout)[0]

    # Retrieve the Link Quality and Signal Level metrics from the extracted output line. The "[::2]" slices the list of RegEx matches, returning a shallow copy containing only the even-indexed elements, which are the values we need.
    wifi_signal_data = []
    if (len(desired_iwconfig_output) == 0):
        wifi_signal_data = ["N/A", "N/A"]
    else:
        wifi_signal_data = re.findall(r"-?[0-9]+", desired_iwconfig_output[0])[::2]
    #print("RegEx results count:", len(wifi_signal_data))
    if (len(wifi_signal_data) == 2):
        print("Link Quality: ", wifi_signal_data[0], "/70, Signal Level: ", wifi_signal_data[1], " dBm", sep="")
    else:
        wifi_signal_data = ["N/A", "N/A"]

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

    # --- Data Output ---
    # Send the retrieved data to the Logger service.
    data_string = f"{wifi_signal_data[0]} {wifi_signal_data[1]} {magnet_x:.6f} {magnet_y:.6f} {magnet_z:.6f}"
    #data_string = f"62 -46 0.356254 -1.595278 0.004625\n"
    data_stream.sendall(data_string.encode('utf-8'))
    #data_stream.sendall(b"Hello, world")
    #data = data_stream.recv(1024)
    #print(f"Received: {data.decode('utf-8')}")





# Process 1: 'iwconfig wlan0'
#p1 = subprocess.Popen(['iwconfig', 'wlan0'], stdout=subprocess.PIPE)

# Process 2: 'grep -E "Link Quality"' (receives stdout from p1)
#p2 = subprocess.Popen(['grep', '-E', '".{0,0}Link Quality=.{0,10}"'], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)

# Allow p1 to receive a SIGPIPE if p2 exits early
#p1.stdout.close()

# Run the pipeline and get the final result
#output, error = p2.communicate()

#print(output)
