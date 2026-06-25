import os
import json
import urllib.request
from mcp.agriculture_mcp import KNOWLEDGE_BASE

class WeatherMCP:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def call_gemini(self, prompt):
        if not self.api_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return json.loads(res_data["candidates"][0]["content"]["parts"][0]["text"].strip())
        except Exception:
            return None

    def query_irrigation_planning(self, state, district, soil_type, crop, temp, humidity, rainfall):
        prompt = f"""
        Weather MCP: Determine irrigation actions and weather risk alerts for:
        Crop: {crop}, Soil: {soil_type} in {district}, {state}.
        Metrics: Temp: {temp}°C, Humidity: {humidity}%, Rainfall: {rainfall}mm.
        
        Return JSON:
        {{
          "irrigation": "specific irrigation recommendation",
          "alert": "weather risk alert"
        }}
        """
        res = self.call_gemini(prompt)
        if res and "irrigation" in res and "alert" in res:
            return res

        # Fallback rules
        crop_clean = crop.lower().strip()
        if "bajra" in crop_clean or "millet" in crop_clean:
            crop_clean = "bajra (pearl millet)"

        # Irrigation
        if rainfall > 100:
            irrigation = f"Suspend irrigation. Heavy rainfall ({rainfall} mm) is more than sufficient. Clear drainage channels to prevent waterlogging."
        elif rainfall > 30:
            irrigation = f"Delay irrigation due to moderate/heavy rainfall ({rainfall} mm). Monitor crop needs."
        elif rainfall > 10:
            irrigation = f"Delay/reduce scheduled irrigation. Recent rainfall of {rainfall} mm provides partial soil moisture."
        else:
            irrigation = f"Irrigate as per routine scheduling. Dry conditions ({rainfall} mm rainfall) require regular monitoring of soil moisture."

        # Risk Alerts
        alerts = []
        info = KNOWLEDGE_BASE.get(crop_clean)
        if info:
            min_opt, max_opt = info["temp_range"]
            if temp > max_opt:
                alerts.append(f"High temperature of {temp}°C exceeds the optimal range ({min_opt}-{max_opt}°C), which may cause heat stress.")
            elif temp < min_opt:
                alerts.append(f"Low temperature of {temp}°C is below optimal ({min_opt}-{max_opt}°C), which might delay crop growth.")
            
            if humidity >= info["rust_risk_humidity"]:
                alerts.append(f"Relative humidity is high ({humidity}%), creating optimal conditions for fungal/disease outbreaks (e.g., rusts, mildews, or blights).")
        
        if not alerts:
            alerts.append("No critical weather risk alerts at this time. Maintain routine monitoring.")

        return {
            "irrigation": irrigation,
            "alert": " ".join(alerts)
        }
