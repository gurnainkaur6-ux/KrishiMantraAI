import os
import unittest
import sys

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.soil_agent import SoilAgent
from agents.weather_agent import WeatherAgent
from agents.pesticide_agent import PesticideSafetyAgent

class TestAgents(unittest.TestCase):
    def test_soil_agent(self):
        agent = SoilAgent()
        res = agent.recommend("Punjab", "Ludhiana", "Loamy", "Wheat")
        self.assertIn("Wheat", res["crop1"])
        self.assertEqual(res["crop2"], "Maize")
        self.assertIn("120 kg Urea", res["npk"])

    def test_weather_agent(self):
        agent = WeatherAgent()
        res = agent.analyze("Punjab", "Ludhiana", "Loamy", "Wheat", 28, 60, 120)
        self.assertIn("Suspend irrigation", res["irrigation"])

    def test_pesticide_agent(self):
        agent = PesticideSafetyAgent()
        res = agent.recommend("Assam", "Tea")
        self.assertIn("Propargite", res["dosage"])
        self.assertIn("7-14 days", res["waiting_period"])

if __name__ == '__main__':
    unittest.main()
