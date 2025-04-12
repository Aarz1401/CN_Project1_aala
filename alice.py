import socket
import os

CHUNK_SIZE = 1024  # Define your chunk size

# Define CHUNK_DIR as a subfolder relative to the script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(SCRIPT_DIR, "chunks")

# Define tracker server location
TRACKER_HOST = "localhost"
TRACKER_PORT = 9000

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

# Function to register file chunks with the tracker
def register_with_tracker(filename, chunk_mapping):
    print(f"Registering {filename} with tracker...")
    
    # Format the data to send to the tracker
    # Create a mapping of chunk_id to (host, port) for each chunk
    chunk_to_peer_map = {}
    
    for chunk_id, peer_info in chunk_mapping.items():
        chunk_to_peer_map[chunk_id] = peer_info
    
    # Connect to the tracker and send the mapping
    with socket.socket() as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        message = f"{filename}:{chunk_to_peer_map}"
        s.sendall(message.encode())
        print(f"Registered {filename} with tracker")

# Main run function
if __name__ == "__main__":
    file_path = "testfile.txt"  #testfile 
    
    # Chunk the file and save it in the "chunks" folder
    chunks = chunk_file(file_path)
    print(f"File has been split into {len(chunks)} chunks")

    # List of peers to send chunks to
    peers = [("localhost", 8001), ("localhost", 8002), ("localhost", 8003), ("localhost", 8004)]
    
    # Dictionary to track which peer has which chunk
    chunk_mapping = {}

    # Sending each chunk to peers
    for i, _ in enumerate(chunks):
        chunk_id = f"chunk_{i}"
        peer = peers[i % len(peers)]  # Alternating between peers
        
        # Send the chunk to the peer
        send_chunk(peer[0], peer[1], chunk_id)
        
        # Record which peer has this chunk
        chunk_mapping[chunk_id] = peer


    # Register the file and its chunk distribution with the tracker
    register_with_tracker(os.path.basename(file_path), chunk_mapping)
    
    print(f"\nFile sharing complete!")
    print(f"File {file_path} has been split into {len(chunks)} chunks and distributed across {len(peers)} peers")
    print(f"Chunk distribution has been registered with the tracker")