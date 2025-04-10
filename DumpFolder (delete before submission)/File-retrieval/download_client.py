import requests
import os

TRACKER_URL = "http://localhost:5000/get_peers"

def get_chunk_locations(file_id):
    response = requests.get(f"{TRACKER_URL}?file_id={file_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to contact tracker.")

def download_chunk(peer_address, chunk_name, output_dir):
    url = f"http://{peer_address}/chunks/{chunk_name}"
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, chunk_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {chunk_name} from {peer_address}")
        return True
    return False

def download_all_chunks(chunk_locations, output_dir="chunks"):
    for chunk_name, peers in chunk_locations.items():
        success = False
        for peer in peers:
            try:
                if download_chunk(peer, chunk_name, output_dir):
                    success = True
                    break
            except Exception as e:
                print(f"Error with peer {peer}: {e}")
        if not success:
            raise Exception(f"Could not download {chunk_name}")

def reconstruct_file(chunks_dir, output_file, num_chunks):
    with open(output_file, 'wb') as output:
        for i in range(num_chunks):
            chunk_file = os.path.join(chunks_dir, f"chunk_{i}")
            with open(chunk_file, 'rb') as chunk:
                output.write(chunk.read())
    print(f"File reconstructed as '{output_file}'")

if __name__ == "__main__":
    file_id = "example_file"
    chunk_dir = "chunks"
    output_file = "reconstructed_file.txt"

    locations = get_chunk_locations(file_id)
    download_all_chunks(locations, chunk_dir)
    reconstruct_file(chunk_dir, output_file, len(locations))

