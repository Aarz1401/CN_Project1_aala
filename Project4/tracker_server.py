import socket

# Dictionary to store filename-to-peer mapping
tracker_data = {}

# Create a TCP socket
s = socket.socket()

# Bind the socket to localhost on port 9000
s.bind(("localhost", 9000))

# Start listening for incoming connections (max 5 queued connections)
s.listen(5)

# Inform that the tracker server is running
print("Tracker is running...")

# Continuously accept and process incoming connections
while True:
    # Accept a connection from a peer
    conn, addr = s.accept()
    
    # Receive data (up to 4096 bytes) and decode it
    data = conn.recv(4096).decode()
    
    # Handle registration messages (from Alice)
    if ":" in data and not data.startswith("REQUEST"):
        # Split the data into filename and the mapping string
        filename, mapping = data.split(":", 1)
        
        # Update the tracker dictionary with the new mapping
        tracker_data[filename] = eval(mapping)
        
        # Print the updated mapping
        print(f"Updated tracker for {filename}: {tracker_data[filename]}")
    
    # Handle requests from Bob
    elif data.startswith("REQUEST:"):
        # Parse the requested filename
        _, filename = data.split(":", 1)
        
        print(f"Received request for file: {filename}")
        
        # Check if the file exists in our tracker database
        if filename in tracker_data:
            # Send the peer mapping information
            response = str(tracker_data[filename])
            conn.sendall(response.encode())
            print(f"Sent chunk mapping for {filename}")
        else:
            # File not found
            conn.sendall(f"ERROR:File {filename} not found".encode())
            print(f"File {filename} not found in tracker database")
    
    # Close the connection
    conn.close()
