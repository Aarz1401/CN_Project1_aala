import os
import json
import requests

CONFIG = json.load(open("tracker_config.json"))
FILE_ID = CONFIG["file_id"]
TRACKER_URL = f"http://localhost:{CONFIG['tracker_port']}"

def get_chunk_locations():
    response = requests.get(f"{TRACKER_URL}/get_peers?file_id={FILE_ID}")
    return response.json()

def download_chunk(peer, chunk, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    url = f"http://{peer}/chunks/{chunk}"
    r = requests.get(url)
    if r.status_code == 200:
        with open(f"{out_dir}/{chunk}", 'wb') as f:
            f.write(r.content)
        print(f"Downloaded {chunk} from {peer}")
        return True
    return False

def download_all_chunks(chunk_locations, out_dir="chunks"):
    for chunk, peers in chunk_locations.items():
        for peer in peers:
            if download_chunk(peer, chunk, out_dir):
                break

def reconstruct_file(out_file="reconstructed_file.txt", chunks_dir="chunks"):
    with open(out_file, 'wb') as f_out:
        for i in range(len(os.listdir(chunks_dir))):
            with open(f"{chunks_dir}/chunk_{i}", 'rb') as f:
                f_out.write(f.read())
    print(f"Reconstructed file saved as {out_file}")

if __name__ == "__main__":
    locations = get_chunk_locations()
    download_all_chunks(locations)
    reconstruct_file()
