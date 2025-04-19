import httpx
import logging

class MGClientAU:
    def __init__(self, username, password, base_url="https://gateway-mg-au.soimt.com/api.app/v1"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.token = None

    async def login(self):
        url = f"{self.base_url}/user/login"
        payload = {
            "loginAccount": self.username,
            "password": self.password,
            "clientType": 1,
            "loginType": 0,
            "appVersion": "5.3.0",
            "osVersion": "iOS 16.0",
            "deviceType": "iPhone15,3"
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MGApp/5.3.0 (iPhone; iOS 16.0; Scale/3.00)",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "platform": "ios",
            "appId": "10001"
        }

        logging.info(f"POST {url}")
        res = await self.client.post(url, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

        if data.get("code") != 0:
            raise Exception(f"Login error: {data.get('message')}")

        self.token = data["data"]["accessToken"]
        return self.token

    async def get_vehicle_list(self):
        url = f"{self.base_url}/vehicle/my"
        headers = {"accessToken": self.token}
        res = await self.client.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        if not data.get("data"):
            raise Exception("No vehicle found")
        return data["data"][0]

    async def unlock_vehicle(self, vin):
        url = f"{self.base_url}/vehicle/unlock"
        headers = {"accessToken": self.token}
        payload = {
            "vin": vin,
            "deviceType": 0,
            "appFlag": 0
        }
        res = await self.client.post(url, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()