from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open("tracker_db.json") as f:
    TRACKER_DATA = json.load(f)

@app.route("/get_peers", methods=["GET"])
def get_peers():
    file_id = request.args.get("file_id")
    return jsonify(TRACKER_DATA.get(file_id, {}))

if __name__ == "__main__":
    config = json.load(open("tracker_config.json"))
    app.run(port=config["tracker_port"])
