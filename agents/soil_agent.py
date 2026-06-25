from mcp.agriculture_mcp import AgricultureKnowledgeMCP

class SoilAgent:
    def __init__(self):
        self.mcp = AgricultureKnowledgeMCP()

    def recommend(self, state, district, soil_type, crop):
        # Query suitability from Agriculture Knowledge MCP
        suitability = self.mcp.query_crop_suitability(state, district, soil_type, crop)
        # Query fertilization reference
        fertilizer = self.mcp.query_fertilizer_reference(crop, soil_type)
        
        return {
            "crop1": suitability["crop1"],
            "crop2": suitability["crop2"],
            "organic": fertilizer["organic"],
            "npk": fertilizer["npk"]
        }
