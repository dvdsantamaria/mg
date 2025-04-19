from flask import Flask, jsonify
import os
import asyncio
import logging
from saic_ismart_client_ng.api.auth import MGClientAU

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

USERNAME = os.getenv("MG_USERNAME")
PASSWORD = os.getenv("MG_PASSWORD")

@app.route("/", methods=["GET"])
def home():
    return "✅ MG API AU lista - /unlock disponible"

@app.route("/unlock", methods=["GET"])
def unlock():
    async def process():
        client = MGClientAU(USERNAME, PASSWORD)
        await client.login()
        vehicle = await client.get_vehicle_list()
        vin = vehicle["vin"]
        unlock_result = await client.unlock_vehicle(vin)
        return {
            "vin": vin,
            "result": unlock_result
        }

    try:
        result = asyncio.run(process())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)