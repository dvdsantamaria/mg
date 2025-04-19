import httpx
import logging

class MGClientAU:
    def __init__(self, username, password, base_url="https://tap-au.soimt.com"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.token = None

    async def login(self):
        url = f"{self.base_url}/api/user/login"
        payload = {
            "loginAccount": self.username,
            "password": self.password,
            "clientType": 1,
            "loginType": 0,
            "appVersion": "1.0.0",
            "osVersion": "iOS 16.0",
            "deviceType": "iPhone15,3"
        }

        logging.info(f"POST {url}")
        res = await self.client.post(url, json=payload)
        res.raise_for_status()
        data = res.json()
        self.token = data["data"]["accessToken"]
        return self.token

    async def get_vehicle_list(self):
        url = f"{self.base_url}/api/vehicle/my"
        headers = {"accessToken": self.token}
        res = await self.client.get(url, headers=headers)
        res.raise_for_status()
        return res.json()["data"][0]  # primer vehículo

    async def unlock_vehicle(self, vin):
        url = f"{self.base_url}/api/vehicle/unlock"
        headers = {"accessToken": self.token}
        payload = {
            "vin": vin,
            "deviceType": 0,
            "appFlag": 0
        }
        res = await self.client.post(url, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()