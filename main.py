from flask import Flask, request, jsonify
import os

app = Flask(__name__)

bin_data = {}
with open("vbvbin.txt", "r") as f:
    for line in f:
        parts = line.strip().split("|", 1)
        if len(parts) >= 2:
            bin_number = parts[0]
            bin_data[bin_number] = line.strip()

@app.route("/gateway=bin", methods=["GET"])
def check_bin():
    key = request.args.get("key", "")
    card = request.args.get("card", "")

    if key != "alwayswiz":
        return jsonify({"error": "Invalid API key"}), 403

    if not card or len(card) < 6:
        return jsonify({"error": "Invalid card format"}), 400

    bin_number = card[:6]

    result_line = bin_data.get(bin_number)
    if not result_line:
        return jsonify({"bin": bin_number, "response": "BIN not found in database"})

    parts = result_line.split("|")

    if len(parts) >= 3:
        response = parts[2].strip()
    else:
        response = "Unknown"

    return jsonify({"bin": bin_number, "response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
