import socket
import os

HOST = "localhost"
PORT = 8003  # Change to 8002 for second peer

# Define the directory for storing received chunks
CHUNK_DIR = f"peer_{PORT}_chunks"

# Create the directory if it doesn't exist
os.makedirs(CHUNK_DIR, exist_ok=True)

# Set up the socket
s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)

print(f"Peer running on port {PORT}")

while True:
    conn, addr = s.accept()
    data = conn.recv(2048)
    
    # Split received data into chunk ID and chunk content
    chunk_id, chunk = data.split(b'||', 1)
    
    # Define the path for saving the chunk in the CHUNK_DIR folder
    chunk_file_path = os.path.join(CHUNK_DIR, f"{chunk_id.decode()}")
    
    # Save the chunk to the specified directory
    with open(chunk_file_path, "wb") as f:
        f.write(chunk)
    
    print(f"Stored {chunk_id.decode()} in {CHUNK_DIR}")
    conn.close()
