import os
import json
import sys

MEMORY_FILE = "context_memory.json"

class ContextManager:
    def __init__(self, memory_file=MEMORY_FILE):
        self.memory_file = memory_file
        self.data = {
            "state": None,
            "district": None,
            "soil_type": None,
            "crop": None,
            "temperature": None,
            "humidity": None,
            "rainfall": None
        }
        self.load()

    def load(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    saved_data = json.load(f)
                    for key in self.data:
                        if key in saved_data:
                            self.data[key] = saved_data[key]
            except Exception as e:
                print(f"Error loading context memory: {e}", file=sys.stderr)

    def save(self):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving context memory: {e}", file=sys.stderr)

    def is_complete(self):
        return all(v is not None for v in self.data.values())

    def get_missing_fields(self):
        return [k for k, v in self.data.items() if v is None]
