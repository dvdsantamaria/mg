from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

MG_EMAIL = os.getenv("MG_EMAIL")
MG_PASSWORD = os.getenv("MG_PASSWORD")
MG_VIN = os.getenv("MG_VIN")

LOGIN_URL = "https://eu-ccapi.gwm-cloud.com/api/auth/login"
BASE_API_URL = "https://eu-ccapi.gwm-cloud.com/api/vehicle"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "mgapp/5.7.0 (iOS 16.1)",
}


def get_token():
    login_payload = {
        "userAccount": MG_EMAIL,
        "password": MG_PASSWORD,
        "loginType": 0,
        "clientId": "client-id-placeholder",
        "deviceId": "device-id-placeholder",
        "appVersion": "5.7.0",
        "osType": "iOS",
        "osVersion": "16.1",
        "lang": "en"
    }
    login_response = requests.post(LOGIN_URL, json=login_payload, headers=HEADERS)
    login_response.raise_for_status()
    return login_response.json().get("accessToken")


@app.route("/open-car", methods=["GET"])
def open_car():
    try:
        token = get_token()
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        payload = {"vin": MG_VIN, "deviceType": 1}
        response = requests.post(f"{BASE_API_URL}/unlock", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"status": "Car unlocked successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/lock-car", methods=["GET"])
def lock_car():
    try:
        token = get_token()
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        payload = {"vin": MG_VIN, "deviceType": 1}
        response = requests.post(f"{BASE_API_URL}/lock", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"status": "Car locked successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
