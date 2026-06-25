from mcp.weather_mcp import WeatherMCP

class WeatherAgent:
    def __init__(self):
        self.mcp = WeatherMCP()

    def analyze(self, state, district, soil_type, crop, temp, humidity, rainfall):
        return self.mcp.query_irrigation_planning(
            state, district, soil_type, crop, temp, humidity, rainfall
        )
