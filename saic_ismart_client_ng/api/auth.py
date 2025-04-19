class Auth:
    def __init__(self, region="AU"):
        if region == "AU":
            self.base_url = "https://tap-au.soimt.com"
        else:
            raise ValueError(f"Región {region} no soportada")

    def login_url(self):
        return f"{self.base_url}/api/user/login"
