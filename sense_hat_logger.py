import socket

HOST_IP = "127.0.0.1"  # the hostname of this Logger service's container
HOST_PORT = 41000      # the port that the Logger service listens on

# Create and bind a socket to use for communication with the Data Polling service.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
    data_socket.bind((HOST_IP, HOST_PORT))

    # Listen for incoming connections.
    data_socket.listen()

    # Accept an incoming connection.
    data_conn, data_addr = data_socket.accept()
    with data_conn:
        print(f"Connected by {data_addr}")

        # Continuously check if any new data has been received.
        while True:
            # Read any available bytes from the socket's buffer.
            data_bytes = data_conn.recv(4096)

            # Check if the connection has been closed (which causes socket.recv() to return an empty bytes object).
            if not data_bytes:
                break

            # Reconstruct the transmitted string from the received bytes.
            data_string = data_bytes.decode('utf-8')

            # Slice the string to extract each data point.
            data_vals = data_string.split(" ")
            print(f"Link Quality: {data_vals[0]}/70, Signal Level: {data_vals[1]} dBm, Magnetometer: ({data_vals[2]} µT, {data_vals[3]} µT, {data_vals[4]} µT)")
            #data_conn.sendall(data_bytes)  # Echo back received bytes
