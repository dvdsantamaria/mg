from flask import Flask, jsonify
import os
import asyncio
import logging
from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration

app = Flask(__name__)

# Variables de entorno
USERNAME = os.getenv("MG_USERNAME")
PASSWORD = os.getenv("MG_PASSWORD")

# Logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def root():
    return "✅ MG Unlock API está corriendo"

@app.route("/unlock", methods=["GET"])
def unlock():
    async def unlock_vehicle():
        config = SaicApiConfiguration(username=USERNAME, password=PASSWORD)
        saic_api = SaicApi(config)
        await saic_api.login()
        vehicles = await saic_api.vehicle_list()
        vin = vehicles.vinList[0].vin
        await saic_api.unlock_vehicle(vin)
        return {"status": "Vehículo desbloqueado", "vin": vin}

    try:
        result = asyncio.run(unlock_vehicle())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)