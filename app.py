#!/usr/bin/env python3
"""
KrishiMitra AI: Indian Agriculture Multi-Agent Decision Support System
Main orchestrating module.
"""
import os
import sys
import json

# Setup module path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.context_manager import ContextManager
from agents.soil_agent import SoilAgent
from agents.weather_agent import WeatherAgent
from agents.pesticide_agent import PesticideSafetyAgent

ENV_FILE = ".env"
UNSAFE_KEYWORDS = [
    "double dose",
    "10x",
    "excessive pesticide",
    "kill faster",
    "overdose",
    "maximum chemical"
]

def load_env(env_file=ENV_FILE):
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
        except Exception as e:
            print(f"Warning: Failed to load .env file: {e}", file=sys.stderr)

# Load env configurations
load_env()

def check_security_guardrail(inputs):
    for key, value in inputs.items():
        if value:
            val_str = str(value).lower()
            for kw in UNSAFE_KEYWORDS:
                if kw in val_str:
                    print("⚠️ CRITICAL SECURITY VIOLATION: UNSAFE DOSAGE DETECTED. Excessive pesticide application destroys crop systems and violates environmental laws. Consult local KVK authorities immediately.")
                    sys.exit(1)

def format_report(soil_report, weather_report, pesticide_report, context_file_path):
    output = []
    output.append("### SOIL REPORT\n")
    output.append(f"* Crop 1: {soil_report['crop1']}")
    output.append(f"* Crop 2: {soil_report['crop2']}")
    output.append(f"* Organic: {soil_report['organic']}")
    output.append(f"* NPK: {soil_report['npk']}\n")

    output.append("### WEATHER REPORT\n")
    output.append(f"* Irrigation: {weather_report['irrigation']}")
    output.append(f"* Alert: {weather_report['alert']}\n")

    output.append("### PESTICIDE REPORT\n")
    output.append(f"* Dosage: {pesticide_report['dosage']}")
    output.append(f"* Waiting Period: {pesticide_report['waiting_period']}")
    output.append(f"* Safety: {pesticide_report['safety']}\n")

    abs_path = os.path.abspath(context_file_path).replace("\\", "/")
    file_link = f"[context_memory.json](file:///{abs_path})"

    output.append("### FINAL RECOMMENDATION\n")
    output.append(f"* [ ] Inspect crop leaves regularly for anomalies based on weather alerts.")
    output.append(f"* [ ] Adjust irrigation application in response to rainfall and soil moisture.")
    output.append(f"* [ ] Update crop parameters as needed in the local state storage at {file_link}.")
    
    return "\n".join(output)

def main():
    manager = ContextManager()
    
    # Read CLI args
    if len(sys.argv) > 1:
        cli_inputs = {}
        for arg in sys.argv[1:]:
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.lower().strip()
                v = v.strip()
                if k in manager.data:
                    if k in ["temperature", "humidity", "rainfall"]:
                        try:
                            v = float(v) if '.' in v else int(v)
                        except ValueError:
                            pass
                    cli_inputs[k] = v
        
        # Check safety
        check_security_guardrail(cli_inputs)
        
        # Save memory
        for k, v in cli_inputs.items():
            manager.data[k] = v
        manager.save()

    # Retrieve missing fields
    missing = manager.get_missing_fields()
    if missing:
        print("Missing required fields. Please specify them via CLI arguments (e.g. state=Punjab) or input them below:")
        interactive_updates = {}
        for field in missing:
            val = input(f"Enter {field.replace('_', ' ').title()}: ").strip()
            if not val:
                print(f"Error: {field} is required.")
                sys.exit(1)
            if field in ["temperature", "humidity", "rainfall"]:
                try:
                    val = float(val) if '.' in val else int(val)
                except ValueError:
                    pass
            interactive_updates[field] = val
        
        # Check safety on updates
        check_security_guardrail(interactive_updates)
        
        # Save memory
        for k, v in interactive_updates.items():
            manager.data[k] = v
        manager.save()

    # Final guardrail validation
    check_security_guardrail(manager.data)

    # Initialize Agents
    soil_agent = SoilAgent()
    weather_agent = WeatherAgent()
    pesticide_agent = PesticideSafetyAgent()

    # Extract parameters
    state = manager.data["state"]
    district = manager.data["district"]
    crop = manager.data["crop"]
    soil_type = manager.data["soil_type"]
    temp = manager.data["temperature"]
    humidity = manager.data["humidity"]
    rainfall = manager.data["rainfall"]

    # Generate Reports
    soil_rep = soil_agent.recommend(state, district, soil_type, crop)
    weather_rep = weather_agent.analyze(state, district, soil_type, crop, temp, humidity, rainfall)
    pesticide_rep = pesticide_agent.recommend(state, crop)

    # Render results
    report = format_report(soil_rep, weather_rep, pesticide_rep, manager.memory_file)
    print(report)

if __name__ == "__main__":
    main()
