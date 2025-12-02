import requests
import os

API_KEY = os.getenv("f36faaec08a2cdf58fe85cc986510752f8e1b45d")  # ты через Railway ENV задашь

def get_aqi(city: str):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if data.get("status") != "ok":
            return None

        return data["data"]["aqi"]

    except Exception:
        return None
