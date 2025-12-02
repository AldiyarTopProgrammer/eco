from pwaqi import AirQuality

API_KEY = "f36faaec08a2cdf58fe85cc986510752f8e1b45d"

def get_aqi(city: str):
    aqi = AirQuality(api_key=API_KEY)
    result = aqi.city(city)

    if not result or "data" not in result:
        return None

    return result["data"]["aqi"]
