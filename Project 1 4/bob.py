import socket
import os
import time

# Define constants
TRACKER_HOST = "localhost"
TRACKER_PORT = 9000
CHUNK_DIR = "bob_received_chunks"
OUTPUT_FILE = "bob_received_file.txt"

# Create directory for received chunks if it doesn't exist
os.makedirs(CHUNK_DIR, exist_ok=True)

def get_peer_info_from_tracker(filename):
    """
    Contact the tracker to get information about where chunks are stored
    
    Args:
        filename: Name of the file to retrieve
        
    Returns:
        Dictionary mapping chunk IDs to peer information
    """
    print(f"Contacting tracker for file: {filename}...")
    
    # Connect to the tracker server
    with socket.socket() as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        
        # Send request for the file
        request = f"REQUEST:{filename}"
        s.sendall(request.encode())
        
        # Receive response from tracker
        response = s.recv(4096).decode()
        
        if response.startswith("ERROR"):
            print(f"Tracker error: {response}")
            return None
        
        # Parse the chunk-to-peer mapping from the response
        try:
            chunk_mapping = eval(response)
            print(f"Received chunk mapping from tracker: {chunk_mapping}")
            return chunk_mapping
        except:
            print("Error parsing tracker response")
            return None

def fetch_chunk_from_peer(peer_host, peer_port, chunk_id):
    """
    Retrieve a specific chunk from a peer
    
    Args:
        peer_host: Hostname of the peer
        peer_port: Port number of the peer
        chunk_id: ID of the chunk to retrieve
        
    Returns:
        The chunk data if successful, None otherwise
    """
    print(f"Fetching {chunk_id} from {peer_host}:{peer_port}...")
    
    try:
        # Connect to the peer
        with socket.socket() as s:
            s.connect((peer_host, peer_port))
            
            # Request the chunk
            request = f"GET:{chunk_id}"
            s.sendall(request.encode())
            
            # Receive the chunk data
            chunk_data = s.recv(2048)
            
            # Check if the response contains the chunk data
            if b'||' in chunk_data:
                _, chunk = chunk_data.split(b'||', 1)
                return chunk
            else:
                print(f"Invalid response from peer for {chunk_id}")
                return None
    except Exception as e:
        print(f"Error fetching chunk {chunk_id}: {e}")
        return None

def download_chunks(chunk_mapping):
    """
    Download all chunks from their respective peers
    
    Args:
        chunk_mapping: Dictionary mapping chunk IDs to peer information
        
    Returns:
        List of chunk IDs successfully downloaded, in order
    """
    successful_chunks = []
    
    # Process the chunk mapping to retrieve each chunk
    for chunk_id, peer_info in chunk_mapping.items():
        peer_host, peer_port = peer_info
        
        # Try to fetch the chunk from the peer
        chunk_data = fetch_chunk_from_peer(peer_host, peer_port, chunk_id)
        
        if chunk_data:
            # Save the chunk to our local directory
            chunk_path = os.path.join(CHUNK_DIR, chunk_id)
            with open(chunk_path, "wb") as f:
                f.write(chunk_data)
            
            successful_chunks.append(chunk_id)
            print(f"Successfully saved {chunk_id}")
        else:
            print(f"Failed to download {chunk_id}")
    
    return successful_chunks
    
def reconstruct_file(chunk_ids):
    """
    Reconstruct the original file from downloaded chunks
    
    Args:
        chunk_ids: List of chunk IDs to combine, in order
        
    Returns:
        True if file reconstruction was successful, False otherwise
    """
    try:
        # Sort chunks by their numerical ID to ensure correct order
        sorted_chunks = sorted(chunk_ids, key=lambda x: int(x.split('_')[1]))
        
        print(f"Reconstructing file from {len(sorted_chunks)} chunks...")
        print(f"Chunks will be assembled in the following order: {sorted_chunks}")
        
        # Combine all chunks into the output file
        total_bytes = 0
        with open(OUTPUT_FILE, "wb") as outfile:
            for i, chunk_id in enumerate(sorted_chunks):
                chunk_path = os.path.join(CHUNK_DIR, chunk_id)
                with open(chunk_path, "rb") as infile:
                    chunk_data = infile.read()
                    chunk_size = len(chunk_data)
                    total_bytes += chunk_size
                    outfile.write(chunk_data)
                print(f"Added chunk {i+1}/{len(sorted_chunks)}: {chunk_id} ({chunk_size} bytes)")
        
        print(f"File reconstruction complete! Saved as {OUTPUT_FILE}")
        print(f"Total file size: {total_bytes} bytes")
        print(f"You can view the file by opening: {os.path.abspath(OUTPUT_FILE)}")
        return True
    except Exception as e:
        print(f"Error reconstructing file: {e}")
        return False
def main():
    """Main function to orchestrate the file retrieval process"""
    print("Starting Bob's file retrieval process...")
    
    # For this example, we're retrieving "testfile.txt" that Alice shared
    filename = "testfile.txt"
    
    # Step 1: Get chunk-to-peer mapping from tracker
    chunk_mapping = get_peer_info_from_tracker(filename)
    if not chunk_mapping:
        print("Failed to get chunk information from tracker. Exiting.")
        return
    
    # Step 2: Download all chunks from peers
    successful_chunks = download_chunks(chunk_mapping)
    if not successful_chunks:
        print("Failed to download any chunks. Exiting.")
        return
    
    # Step 3: Reconstruct the original file
    reconstruct_file(successful_chunks)
    
    print("\nFile retrieval and reconstruction complete!")
    print(f"Original file reconstructed as: {OUTPUT_FILE}")

if __name__ == "__main__":
    # Give a moment for all peers to start up
    time.sleep(1)
    main()