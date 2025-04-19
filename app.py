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
    raise EnvironmentError("MG_USERNAME y MG_PASSWORD deben estar definidos en Railway.")

@app.route("/", methods=["GET"])
def home():
    return "✅ MG Unlock API corriendo - listo para testear regiones."

@app.route("/unlock", methods=["GET"])
def unlock():
    async def try_unlock_with_base(base_url):
        logging.info(f"Probando login con base_url: {base_url}")
        config = SaicApiConfiguration(username=USERNAME, password=PASSWORD, base_url=base_url)
        saic_api = SaicApi(config)
        await saic_api.login()
        vehicles = await saic_api.vehicle_list()
        vin = vehicles.vinList[0].vin
        await saic_api.unlock_vehicle(vin)
        return {"status": "Vehículo desbloqueado", "vin": vin, "base_url": base_url}

    async def unlock_with_fallback():
        try:
            return await try_unlock_with_base("https://capi-ap-eas-1.mgapi.io")
        except Exception as ap_err:
            logging.warning(f"Falló región APAC: {ap_err}")
            try:
                return await try_unlock_with_base("https://capi-eu.myconnectedcar.io")
            except Exception as eu_err:
                logging.error(f"Falló también con EU: {eu_err}")
                raise eu_err

    try:
        result = asyncio.run(unlock_with_fallback())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)