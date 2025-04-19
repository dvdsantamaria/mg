from flask import Flask, jsonify
import os
import asyncio
import logging
from saic_ismart_client_ng.api.auth import Auth

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

USERNAME = os.getenv("MG_USERNAME")
PASSWORD = os.getenv("MG_PASSWORD")

@app.route("/", methods=["GET"])
def home():
    return "✅ MG Unlock API con endpoint AU"

@app.route("/unlock", methods=["GET"])
def unlock():
    try:
        auth = Auth(region="AU")
        return jsonify({"login_url": auth.login_url(), "status": "Auth preparado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
