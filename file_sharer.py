import os
import json

CONFIG = json.load(open("tracker_config.json"))
FILE_ID = CONFIG["file_id"]
PEERS = CONFIG["peers"]

# Code used for Alice to split file into chunks and distribute them
def chunk_file(filename, chunk_size=50):
    with open(filename, 'rb') as f:
        data = f.read()
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def distribute_chunks(chunks):
    peer_names = list(PEERS.keys())
    os.makedirs("peer_data", exist_ok=True)

    for peer in peer_names:
        os.makedirs(f"peer_data/{peer}/chunks", exist_ok=True)

    file_chunk_map = {}

    for i, chunk in enumerate(chunks):
        chunk_name = f"chunk_{i}"
        file_chunk_map[chunk_name] = []
        for j in range(2):  # each chunk goes to 2 peers
            peer = peer_names[(i + j) % len(peer_names)]
            path = f"peer_data/{peer}/chunks/{chunk_name}"
            with open(path, 'wb') as f:
                f.write(chunk)
            file_chunk_map[chunk_name].append(f"localhost:{PEERS[peer]['port']}")

    # Save to JSON file for the tracker to load
    with open("tracker_db.json", "w") as f:
        json.dump({FILE_ID: file_chunk_map}, f, indent=2)

    print("Chunks distributed and tracker_db.json created.")

if __name__ == "__main__":
    chunks = chunk_file("original_file.txt")
    distribute_chunks(chunks)
