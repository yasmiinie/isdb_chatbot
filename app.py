from flask import Flask, request, jsonify
from flask_cors import CORS
from ch2 import build_chain
import os

app = Flask(__name__)
CORS(app)

chain = build_chain()  # Load once at startup
@app.route("/", methods=["GET"])
def index():
    return "FAS Scenario Classifier is running!", 200

@app.route("/process_fas", methods=["POST"])
def process_fas():
    data = request.get_json()
    scenario = data.get("scenario")

    if not scenario:
        return jsonify({"error": "Scenario is required."}), 400

    try:
        response = chain.run({"scenario": scenario})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
