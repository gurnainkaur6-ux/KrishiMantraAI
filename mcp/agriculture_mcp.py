import os
import json
import urllib.request

# Local rules database fallback
KNOWLEDGE_BASE = {
    "wheat": {
        "crop2": "Maize",
        "organic": "Well-decomposed Farmyard Manure (FYM) or compost at 4-6 tonnes/acre",
        "npk": "120 kg Urea, 55 kg DAP, and 10 kg MOP per acre (adjust based on soil test report)",
        "pesticide": "Propiconazole 25% EC at 200 ml/acre diluted in 200 liters of water (for stripe/yellow rust)",
        "waiting_period": "30 days between final spray and harvest",
        "ppe": "Wear nitrile/chemical-resistant gloves, protective goggles, long pants, a long-sleeved shirt, and boots. Spray in the direction of the wind.",
        "temp_range": (15, 22),
        "rust_risk_humidity": 60
    },
    "rice": {
        "crop2": "Wheat",
        "organic": "Green manuring (dhaincha) or well-decomposed FYM at 6 tonnes/acre",
        "npk": "110 kg Urea, 30 kg DAP, and 20 kg MOP per acre",
        "pesticide": "Tricyclazole 75% WP @ 120 g/acre in 200L water (for blast control) or Streptocycline @ 6 g/acre (BLB)",
        "waiting_period": "28 days",
        "ppe": "Wear protective face shield, rubber gloves, apron, and boots. Do not spray during heavy rains.",
        "temp_range": (22, 35),
        "rust_risk_humidity": 75
    },
    "cotton": {
        "crop2": "Pigeonpea or Soybean",
        "organic": "Compost or Farmyard Manure @ 5 tonnes/acre",
        "npk": "100 kg Urea, 75 kg Single Super Phosphate (SSP), and 30 kg MOP per acre",
        "pesticide": "Spinosad 45% SC @ 60 ml/acre in 200L water (for Bollworm control)",
        "waiting_period": "30 days",
        "ppe": "Wear heavy-duty gloves, protective respirator mask, goggles, and long-sleeved clothing.",
        "temp_range": (20, 32),
        "rust_risk_humidity": 70
    },
    "maize": {
        "crop2": "Finger Millet / Ragi",
        "organic": "FYM or compost @ 4 tonnes/acre",
        "npk": "150 kg Urea, 60 kg DAP, and 30 kg MOP per acre",
        "pesticide": "Chlorantraniliprole 18.5% SC @ 80 ml/acre in 200L water (for Fall Armyworm)",
        "waiting_period": "30 days",
        "ppe": "Wear chemical-resistant gloves, face mask, protective safety glasses, and full body clothing.",
        "temp_range": (18, 30),
        "rust_risk_humidity": 70
    },
    "sugarcane": {
        "crop2": "Mustard or Potato (as intercrops in autumn sowing)",
        "organic": "Pressmud or Farmyard Manure @ 10 tonnes/acre",
        "npk": "120 kg Urea, 80 kg DAP, and 40 kg MOP per acre",
        "pesticide": "Imidacloprid 17.8% SL @ 100 ml/acre in 200L water (for early shoot borer)",
        "waiting_period": "45 days",
        "ppe": "Wear chemical-resistant boots, apron, goggles, and nitrile gloves. Avoid spray drift.",
        "temp_range": (20, 35),
        "rust_risk_humidity": 75
    },
    "groundnut": {
        "crop2": "Pearl Millet or Sesame",
        "organic": "Farmyard Manure @ 4 tonnes/acre",
        "npk": "25 kg Urea, 50 kg DAP, and 20 kg MOP per acre (Apply Gypsum @ 100-150 kg/acre at flowering)",
        "pesticide": "Mancozeb 75% WP @ 400 g/acre in 200L water (for Tikka Leaf Spot control)",
        "waiting_period": "21 days",
        "ppe": "Wear dust mask during mixing, protective gloves, goggles, and long-sleeved clothing.",
        "temp_range": (22, 30),
        "rust_risk_humidity": 65
    },
    "bajra (pearl millet)": {
        "crop2": "Moth Bean or Cluster Bean",
        "organic": "Farmyard Manure @ 2-3 tonnes/acre",
        "npk": "40 kg Urea and 30 kg DAP per acre",
        "pesticide": "Mancozeb 75% WP @ 400 g/acre in 200L water (for Downy Mildew control)",
        "waiting_period": "21 days",
        "ppe": "Use protective face mask, safety glasses, gloves, and protective clothing.",
        "temp_range": (25, 38),
        "rust_risk_humidity": 50
    },
    "tea": {
        "crop2": "Shade trees (Albizia lebbeck / Indigofera teysmannii)",
        "organic": "Neem cake or well-composted organic mulch @ 2 tonnes/acre",
        "npk": "Standard NPK 2:1:2 mixture (~60 kg Nitrogen/acre/year in split applications)",
        "pesticide": "Propargite 57% EC @ 200 ml/acre in 200L water (for Red Spider Mites)",
        "waiting_period": "7-14 days",
        "ppe": "Wear complete PPE (chemical apron, rubber gloves, goggles, and face mask). Spray when bushes are dry.",
        "temp_range": (18, 30),
        "rust_risk_humidity": 80
    }
}

class AgricultureKnowledgeMCP:
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

    def query_crop_suitability(self, state, district, soil_type, crop):
        prompt = f"""
        Agriculture Knowledge MCP: Determine suitability of crop: {crop} for soil type: {soil_type} in {district}, {state}.
        Recommend crop1 suitability and a crop2 alternative/rotation.
        Return JSON:
        {{
          "crop1": "crop suitability details",
          "crop2": "alternative/rotation crop details"
        }}
        """
        res = self.call_gemini(prompt)
        if res and "crop1" in res and "crop2" in res:
            return res

        # Fallback
        crop_clean = crop.lower().strip()
        if "bajra" in crop_clean or "millet" in crop_clean:
            crop_clean = "bajra (pearl millet)"
        info = KNOWLEDGE_BASE.get(crop_clean, {"crop2": "Legumes / Pulses"})
        return {
            "crop1": f"{crop} is highly suitable for {soil_type} soil in {district}, {state}.",
            "crop2": info["crop2"]
        }

    def query_fertilizer_reference(self, crop, soil_type):
        prompt = f"""
        Agriculture Knowledge MCP: Recommend fertilizer application (Organic and chemical NPK) for crop: {crop} in soil: {soil_type}.
        Return JSON:
        {{
          "organic": "organic fertilizer dosage recommendation",
          "npk": "NPK chemical recommendations"
        }}
        """
        res = self.call_gemini(prompt)
        if res and "organic" in res and "npk" in res:
            return res

        # Fallback
        crop_clean = crop.lower().strip()
        if "bajra" in crop_clean or "millet" in crop_clean:
            crop_clean = "bajra (pearl millet)"
        info = KNOWLEDGE_BASE.get(crop_clean, {
            "organic": "Farmyard Manure @ 4 tonnes/acre",
            "npk": "NPK chemical fertilizers according to soil test recommendations"
        })
        return {
            "organic": info["organic"],
            "npk": info["npk"]
        }

    def query_pest_reference(self, crop):
        prompt = f"""
        Agriculture Knowledge MCP: Recommend pesticide treatment compound, waiting period, and safety PPE for crop: {crop}.
        Return JSON:
        {{
          "dosage": "pesticide compound name and safe dosage",
          "waiting_period": "waiting period description",
          "safety": "required PPE description"
        }}
        """
        res = self.call_gemini(prompt)
        if res and all(k in res for k in ["dosage", "waiting_period", "safety"]):
            return res

        # Fallback
        crop_clean = crop.lower().strip()
        if "bajra" in crop_clean or "millet" in crop_clean:
            crop_clean = "bajra (pearl millet)"
        info = KNOWLEDGE_BASE.get(crop_clean, {
            "pesticide": "General bio-pesticides (e.g. neem extract)",
            "waiting_period": "Refer to product label safety instructions",
            "ppe": "Safety gloves, protective face mask, goggles, and shoes."
        })
        return {
            "dosage": info["pesticide"],
            "waiting_period": info["waiting_period"],
            "safety": info["ppe"]
        }
