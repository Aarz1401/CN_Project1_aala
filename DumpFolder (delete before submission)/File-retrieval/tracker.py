import os
import requests

def download_chunk(peer_address, chunk_name, output_dir):
    url = f"http://{peer_address}/chunks/{chunk_name}"  # Assuming peer exposes chunks at this path
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(output_dir, chunk_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {chunk_name} from {peer_address}")
        return True
    return False

def download_all_chunks(chunk_locations, output_dir="chunks"):
    os.makedirs(output_dir, exist_ok=True)
    for chunk_name, peers in chunk_locations.items():
        success = False
        for peer in peers:
            try:
                if download_chunk(peer, chunk_name, output_dir):
                    success = True
                    break
            except Exception as e:
                print(f"Failed to download {chunk_name} from {peer}: {e}")
        if not success:
            raise Exception(f"Could not retrieve {chunk_name} from any peer.")