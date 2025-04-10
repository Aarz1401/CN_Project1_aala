import socket
import os

CHUNK_SIZE = 1024  # Define your chunk size

# Define CHUNK_DIR as a subfolder relative to the script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(SCRIPT_DIR, "chunks")

# Function to chunk the file and save the chunks
def chunk_file(file_path):
    # Ensure the chunk directory exists
    os.makedirs(CHUNK_DIR, exist_ok=True)

    # Open the file and read it as binary data
    with open(file_path, "rb") as f:
        data = f.read()

    # Split data into chunks of CHUNK_SIZE
    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    
    # Save each chunk to the "chunks" folder
    for i, chunk in enumerate(chunks):
        chunk_file_path = os.path.join(CHUNK_DIR, f"chunk_{i}")
        with open(chunk_file_path, "wb") as f:
            f.write(chunk)
    
    return chunks

# Function to send each chunk to a peer
def send_chunk(peer_host, peer_port, chunk_id):
    # Get the path of the chunk
    chunk_file_path = os.path.join(CHUNK_DIR, chunk_id)
    
    # Open the chunk file in binary mode and send it over the network
    with open(chunk_file_path, "rb") as chunk_file:
        chunk = chunk_file.read()

    # Send chunk to the peer
    with socket.socket() as s:
        s.connect((peer_host, peer_port))
        message = f"{chunk_id}".encode() + b'||' + chunk
        s.sendall(message)
        print(f"Sent {chunk_id} to {peer_host}:{peer_port}")

# Example usage
if __name__ == "__main__":
    file_path = "testfile.txt"  # Specify your file path
    
    # Chunk the file and save it in the "chunks" folder
    chunks = chunk_file(file_path)

    # Example: Sending each chunk to peers
    peers = [("localhost", 8001), ("localhost", 8002), ("localhost", 8003), ("localhost", 8004)]

    for i, _ in enumerate(chunks):
        peer = peers[i % len(peers)]  # Alternating between peers
        send_chunk(peer[0], peer[1], f"chunk_{i}")

