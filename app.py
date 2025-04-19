from flask import Flask, jsonify
import os
import asyncio
import logging
from saic_ismart_client_ng import SaicApi
from saic_ismart_client_ng.model import SaicApiConfiguration

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

USERNAME = os.getenv("MG_USERNAME")
PASSWORD = os.getenv("MG_PASSWORD")

if not USERNAME or not PASSWORD:
    raise EnvironmentError("MG_USERNAME y MG_PASSWORD deben estar definidos.")

@app.route("/", methods=["GET"])
def home():
    return "✅ MG Unlock API corriendo"

@app.route("/unlock", methods=["GET"])
def unlock():
    async def try_unlock(region_code):
        logging.info(f"Probando región: {region_code}")
        config = SaicApiConfiguration(username=USERNAME, password=PASSWORD, region=region_code)
        saic_api = SaicApi(config)
        saic_api._auth.BASE_URL = "https://tap-au.soimt.com" 
        await saic_api.login()
        vehicles = await saic_api.vehicle_list()
        vin = vehicles.vinList[0].vin
        await saic_api.unlock_vehicle(vin)
        return {"status": "Vehículo desbloqueado", "vin": vin, "region": region_code}

    async def unlock_with_fallback():
        try:
            return await try_unlock("AP")
        except Exception as ap_err:
            logging.warning(f"Región AP falló: {ap_err}")
            try:
                return await try_unlock("EU")
            except Exception as eu_err:
                logging.error(f"También falló EU: {eu_err}")
                raise eu_err

    try:
        result = asyncio.run(unlock_with_fallback())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)