import os
import unittest
import json
import sys

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.context_manager import ContextManager

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_memory.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = ContextManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_initial_state(self):
        self.assertFalse(self.manager.is_complete())
        self.assertIn("state", self.manager.get_missing_fields())

    def test_save_and_retrieve(self):
        self.manager.data["state"] = "Punjab"
        self.manager.data["district"] = "Ludhiana"
        self.manager.data["soil_type"] = "Loamy"
        self.manager.data["crop"] = "Wheat"
        self.manager.data["temperature"] = 20
        self.manager.data["humidity"] = 50
        self.manager.data["rainfall"] = 10
        self.manager.save()

        # Reload
        new_manager = ContextManager(self.test_file)
        self.assertTrue(new_manager.is_complete())
        self.assertEqual(new_manager.data["state"], "Punjab")
        self.assertEqual(new_manager.data["temperature"], 20)

if __name__ == '__main__':
    unittest.main()
