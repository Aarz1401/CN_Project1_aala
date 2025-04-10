from flask import Flask, send_file
import os
import sys

app = Flask(__name__)
CHUNKS_FOLDER = "chunks"

@app.route("/chunks/<chunk_name>", methods=["GET"])
def get_chunk(chunk_name):
    path = os.path.join(CHUNKS_FOLDER, chunk_name)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return {"error": "Chunk not found"}, 404

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python peer.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    app.run(port=port)

