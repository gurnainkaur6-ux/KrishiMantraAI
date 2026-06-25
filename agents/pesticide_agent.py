from mcp.agriculture_mcp import AgricultureKnowledgeMCP

class PesticideSafetyAgent:
    def __init__(self):
        self.mcp = AgricultureKnowledgeMCP()

    def recommend(self, state, crop):
        return self.mcp.query_pest_reference(crop)
