import socket
import os

# Peer server 3
# Configuration 
HOST = "localhost"
PORT = 8003  

# Directory for storing received chunks
CHUNK_DIR = f"peer_{PORT}_chunks"

# Create the directory 
os.makedirs(CHUNK_DIR, exist_ok=True)

# Set up the socket
s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)

print(f"Peer running on port {PORT}")

while True:
    # Accept connections from Alice (for chunks) or Bob (for requests)
    conn, addr = s.accept()
    data = conn.recv(2048)
    
    # To check if this is a GET request from Bob
    if data.startswith(b'GET:'):
        # Bob is requesting a chunk
        _, chunk_id = data.decode().split(':', 1)
        print(f"Received request for chunk: {chunk_id}")
        
        # to check if we have the requested chunk
        chunk_path = os.path.join(CHUNK_DIR, chunk_id)
        if os.path.exists(chunk_path):
            # Read and send the chunk
            with open(chunk_path, "rb") as f:
                chunk_data = f.read()
            
            # Send the chunk with the proper format
            response = chunk_id.encode() + b'||' + chunk_data
            conn.sendall(response)
            print(f"Sent {chunk_id} to requester at {addr}")
        else:
            # We don't have the requested chunk
            conn.sendall(b"ERROR:Chunk not found")
            print(f"Chunk {chunk_id} not found")
    
    # This is a chunk being sent from Alice
    elif b'||' in data:
        # Split received data into chunk ID and chunk content
        chunk_id, chunk = data.split(b'||', 1)
        
        # Define the path for saving the chunk in the CHUNK_DIR folder
        chunk_file_path = os.path.join(CHUNK_DIR, f"{chunk_id.decode()}")
        
        # Save the chunk to the specified directory
        with open(chunk_file_path, "wb") as f:
            f.write(chunk)
        
        print(f"Stored {chunk_id.decode()} in {CHUNK_DIR}")
    
    # Close the connection
    conn.close()