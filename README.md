# 🌾 KrishiMantra AI
### Multi-Agent Agricultural Decision Support System for Indian Farmers



KrishiMantra AI is an AI-powered Multi-Agent Agricultural Decision Support System designed to help Indian farmers make informed decisions regarding crop planning, soil health, irrigation management, weather-based farming actions, and pesticide safety.

The project demonstrates key AI Agent concepts including Multi-Agent Systems, Agent Skills, MCP-Style Integrations, Context Memory, Security Guardrails, and Agricultural Decision Intelligence.

---

# Problem Statement

Indian farmers often face challenges such as:

- Selecting suitable crops for local soil conditions
- Managing fertilizers efficiently
- Adapting irrigation schedules to changing weather conditions
- Using pesticides safely and responsibly
- Accessing agricultural recommendations from multiple fragmented sources

These challenges can lead to:

- Reduced crop yield
- Water wastage
- Excessive fertilizer usage
- Unsafe pesticide practices
- Increased farming costs

KrishiMantra AI addresses these challenges through a unified AI-powered agricultural assistant.

---

# Why KrishiMantra AI?

Farmers often make critical farming decisions using fragmented information sources. KrishiMantra AI combines crop planning, weather intelligence, soil analysis, irrigation guidance, and pesticide safety into a single AI-powered system that helps farmers make better decisions while promoting sustainable agricultural practices.

---

# Social Impact

KrishiMantra AI supports:

- Sustainable agriculture
- Responsible pesticide usage
- Improved crop productivity
- Water conservation
- Data-driven farming decisions
- Safer farming practices

The project contributes toward smarter and safer agricultural practices for Indian farmers.

---

# System Architecture

```text
                    Farmer
                       │
                       ▼
               KrishiMantra AI
                   Main Agent
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼

 Soil Agent      Weather Agent    Pesticide Agent
      │                │                │
      ▼                ▼                ▼

Agriculture MCP   Weather MCP   Safety Validation
```

---

# Multi-Agent System

The system consists of three specialized agents.

## Soil Agent

Responsibilities:

- Soil analysis
- Crop suitability recommendations
- Organic fertilizer planning
- NPK fertilizer recommendations

Outputs:

- Recommended crops
- Organic fertilizer quantity
- NPK recommendations

---

## Weather Agent

Responsibilities:

- Weather analysis
- Irrigation recommendations
- Heat stress monitoring
- Rainfall analysis

Outputs:

- Irrigation adjustments
- Weather alerts
- Crop risk notifications

---

## Pesticide Safety Agent

Responsibilities:

- Safe pesticide dosage recommendations
- Waiting period guidance
- Farmer safety recommendations

Outputs:

- Dosage per acre
- Waiting period
- PPE requirements

---

#  Agent Skills

KrishiMantra AI demonstrates specialized Agent Skills.

## Soil Analysis Skill

- Soil classification
- Crop matching
- Fertilizer recommendations

## Weather Analysis Skill

- Irrigation planning
- Weather monitoring
- Crop stress analysis

## Pesticide Safety Skill

- Dosage validation
- Waiting period calculations
- Safety compliance

---

#  MCP-Style Integrations

The project demonstrates MCP-inspired integrations for tool interoperability.

## Weather MCP

Provides:

- Temperature context
- Humidity context
- Rainfall context

Used by:

- Weather Agent

---

## Agriculture Knowledge MCP

Provides:

- Crop suitability knowledge
- Soil compatibility references
- Fertilizer recommendations
- Pest management guidance

Used by:

- Soil Agent
- Pesticide Agent

---

#  Context Memory

KrishiMantra AI maintains agricultural context across interactions.

Stored Parameters:

- State
- District
- Soil Type
- Crop
- Temperature
- Humidity
- Rainfall

Features:

✅ Remembers previous inputs

✅ Reuses existing information

✅ Requests only missing fields

✅ Updates stored values automatically

Example:

```text
State: Punjab
District: Ludhiana
Crop: Wheat
```

Later:

```text
Temperature: 31
Humidity: 68
Rainfall: 20
```

The system automatically retains previously supplied information.

---

#  Security Guardrails

Before generating recommendations, the system validates pesticide-related inputs.

Blocked requests include:

- double dose
- overdose
- 10x dosage
- excessive pesticide
- maximum chemical
- kill faster

If detected:

```text
⚠️ CRITICAL SECURITY VIOLATION: UNSAFE DOSAGE DETECTED. Excessive pesticide application destroys crop systems and violates environmental laws. Consult local KVK authorities immediately.
```

No further processing occurs.

---

#  Output Structure

The assistant generates four structured sections.

## SOIL REPORT

- Suitable Crop 1
- Suitable Crop 2
- Organic Fertilizer Recommendation
- NPK Recommendation

---

## WEATHER REPORT

- Irrigation Recommendation
- Weather Alert

---

## PESTICIDE REPORT

- Safe Dosage
- Waiting Period
- Safety Instructions

---

## FINAL RECOMMENDATION

A consolidated recommendation generated from all participating agents.

---

#  Evaluation

The system was tested using multiple agricultural scenarios across different Indian states and soil types.

Sample Test Cases:

| State | Soil Type | Crop |
|---------|---------|---------|
| Punjab | Loamy | Wheat |
| Maharashtra | Black Soil | Cotton |
| Rajasthan | Sandy Soil | Bajra |
| Karnataka | Red Soil | Maize |

Evaluation Criteria:

- Crop suitability recommendations
- Fertilizer recommendations
- Irrigation planning
- Weather risk detection
- Pesticide safety compliance

---

#  Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| AI Model | Gemini API |
| User Interface | Streamlit |
| Context Storage | JSON |
| Architecture | Multi-Agent System |
| Integrations | MCP-Style Connectors |
| Version Control | Git & GitHub |

---

#  Installation

Clone Repository

```bash
git clone https://github.com/gurnainkaur6-ux/KrishiMantraAI.git
cd KrishiMantraAI
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Configure Gemini API Key

```bash
GEMINI_API_KEY=YOUR_API_KEY
```

---

#  Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 📂 Project Structure

```text
KrishiMantraAI/

├── app.py
├── agents/
│   ├── soil_agent.py
│   ├── weather_agent.py
│   └── pesticide_agent.py
│
├── mcp/
│   ├── weather_mcp.py
│   └── agriculture_mcp.py
│
├── memory/
│   └── context_manager.py
│
├── prompts/
│   └── system_prompt.txt
│
├── requirements.txt
├── README.md
└── tests/
```

---

# 📸 Screenshots

### Home Interface
<img width="1902" height="942" alt="image" src="Screenshot 2026-06-25 171618.png" />

<img width="780" height="925" alt="image" src="https://github.com/user-attachments/assets/fe318c06-a0c3-4b8f-ba5b-a98b00c5eebe" />

<img width="632" height="956" alignment="center" alt="image" src="https://github.com/user-attachments/assets/8a59c263-0a52-4c76-95c6-539b2ebf7224" />
<img width="665" height="843" alignment="center" alt="image" src="https://github.com/user-attachments/assets/e4594ba7-8425-4b99-a932-55181d5c6d59" />
<img width="407" height="530" alignment="center" alt="image" src="https://github.com/user-attachments/assets/99223b19-c922-44c6-92ef-4ce63cdca53d" />

# 🎥 Demo Video
(https://youtu.be/-Glqo9Ng_RA?si=IwVvhqvHTib5qyze)

#  Course Concepts Demonstrated

✅ Multi-Agent Systems

✅ Agent Skills

✅ MCP-Style Integrations

✅ Context Management

✅ Security Guardrails

✅ Tool Interoperability

✅ Real-World AI Application



# 📜 License

MIT License

---

# 👩‍💻 Developed By

**Gurnain Kaur**

- BCA Student
- AI & Technology Enthusiast
- Kaggle Learner

Built as part of the **5-Day AI Agents: Intensive Vibe Coding Course With Google**.
