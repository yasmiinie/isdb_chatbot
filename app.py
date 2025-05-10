from flask import Flask, request, jsonify
from flask_cors import CORS
from ch2 import build_chain

app = Flask(__name__)
CORS(app)

chain = build_chain()  # Load once at startup

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
    app.run(debug=True)
