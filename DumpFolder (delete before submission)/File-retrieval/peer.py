from flask import Flask, send_file
import os
import sys
import json

app = Flask(__name__)

@app.route("/chunks/<chunk_name>", methods=["GET"])
def serve_chunk(chunk_name):
    path = os.path.join("chunks", chunk_name)
    if os.path.exists(path):
        return send_file(path)
    return {"error": "Chunk not found"}, 404

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python peer.py <peer_name>")
        sys.exit(1)

    peer_name = sys.argv[1]

    # Move into the peer’s own folder
    os.chdir(f"peer_data/{peer_name}")

    # Load port from config
    with open("../../tracker_config.json") as f:
        port = json.load(f)["peers"][peer_name]["port"]

    print(f"✅ Peer '{peer_name}' running on port {port}...")
    app.run(port=port)
