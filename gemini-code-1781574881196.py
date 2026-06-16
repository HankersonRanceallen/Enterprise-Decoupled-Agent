import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Enterprise-Grade AI Agent with Decoupled Database Memory\n",
    "This notebook demonstrates a production-ready AI agent architecture. Instead of relying solely on the LLM's temporary context window, we decouple the agent's brain from its memory layer.\n",
    "\n",
    "### Why this matters for Production:\n",
    "1. **Session Resilience:** State is tracked in an external data structure (simulating a database like Redis, SQLite, or PostgreSQL). Even if the chat session is destroyed, the user profile and historical interactions survive.\n",
    "2. **State Interception:** We programmatically capture tool execution outputs and save them to the database, ensuring clean record-keeping.\n",
    "3. **Context Optimization:** System instructions are dynamically assembled using historical context, allowing personalization (e.g., remembering preferences) without context window bloat."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 1: Install Required Frameworks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install google-genai requests"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 2: Define Core Cloud Infrastructure Tools"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "\n",
    "def search_city_coordinates(city_name: str) -> dict:\n",
    "    \"\"\"\n",
    "    Resolves a general city name string into its respective latitude and longitude coordinates.\n",
    "    \n",
    "    Args:\n",
    "        city_name (str): The name of the city (e.g., 'Paris', 'Tokyo').\n",
    "    Returns:\n",
    "        dict: A dictionary containing 'latitude' and 'longitude' keys.\n",
    "    \"\"\"\n",
    "    registry = {\n",
    "        \"tokyo\": {\"latitude\": 35.6762, \"longitude\": 139.6503},\n",
    "        \"paris\": {\"latitude\": 48.8566, \"longitude\": 2.3522},\n",
    "        \"london\": {\"latitude\": 51.5074, \"longitude\": -0.1278},\n",
    "        \"new york\": {\"latitude\": 40.7128, \"longitude\": -74.0060}\n",
    "    }\n",
    "    key = city_name.lower().strip()\n",
    "    return registry.get(key, {\"latitude\": 0.0, \"longitude\": 0.0})\n",
    "\n",
    "def get_current_weather(latitude: float, longitude: float) -> str:\n",
    "    \"\"\"\n",
    "    Fetches real-time weather data from cloud systems using explicit geographic metrics.\n",
    "    \"\"\"\n",
    "    if latitude == 0.0 and longitude == 0.0:\n",
    "        return \"Could not parse valid coordinates for this destination.\"\n",
    "        \n",
    "    url = f\"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true\"\n",
    "    try:\n",
    "        res = requests.get(url).json()\n",
    "        if \"current_weather\" in res:\n",
    "            cw = res[\"current_weather\"]\n",
    "            return f\"Temperature: {cw['temperature']}°C | Windspeed: {cw['windspeed']} km/h.\"\n",
    "        return \"Weather service lookup failed.\"\n",
    "    except Exception as e:\n",
    "        return f\"Cloud context connection timeout: {str(e)}\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 3: Setup the Mock Enterprise Database & Decoupled State Agent Loop\n",
    "Here we create a state dictionary tracking `user_preferences` and `session_state`. We use `generate_content` dynamically, passing down saved attributes on every independent execution loop."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "from google import genai\n",
    "from google.genai import types\n",
    "\n",
    "client = genai.Client()\n",
    "\n",
    "# --- ENTERPRISE DATABASE LAYER ---\n",
    "# This simulates an external data store like Redis or SQLite. \n",
    "# It persists even if your specific model sessions are reset or timed out.\n",
    "DATABASE_MOCK = {\n",
    "    \"user_preferences\": {\n",
    "        \"temperature_unit\": \"Celsius\",\n",
    "        \"preferred_activity\": \"walking outside\"\n",
    "    },\n",
    "    \"session_state\": {\n",
    "        \"last_city_searched\": None,\n",
    "        \"last_weather_lookup_data\": None\n",
    "    }\n",
    "}\n",
    "\n",
    "def interact_with_enterprise_agent(user_message: str):\n",
    "    print(f\"👤 User: {user_message}\")\n",
    "    print(\"-\"*60)\n",
    "    \n",
    "    # 1. Fetch data from our persistent storage layer to dynamically construct the system prompt\n",
    "    db_context = (\n",
    "        \"You are an advanced enterprise AI assistant with a decoupled database layer.\\n\"\n",
    "        f\"User System Preferences: {DATABASE_MOCK['user_preferences']}\\n\"\n",
    "        f\"Historical database state from prior interactions: {DATABASE_MOCK['session_state']}\\n\\n\"\n",
    "        \"CRITICAL RULE: If the history context contains the weather data necessary to answer \"\n",
    "        \"the user's follow-up request, DO NOT execute any tool calls again. Reason over the historical text context directly.\"\n",
    "    )\n",
    "    \n",
    "    config = types.GenerateContentConfig(\n",
    "        tools=[search_city_coordinates, get_current_weather],\n",
    "        temperature=0.2,\n",
    "        system_instruction=db_context\n",
    "    )\n",
    "    \n",
    "    # 2. Invoke the stateless engine passing our dynamically hydrated configuration state\n",
    "    response = client.models.generate_content(\n",
    "        model='gemini-2.5-flash',\n",
    "        contents=user_message,\n",
    "        config=config\n",
    "    )\n",
    "    \n",
    "    # 3. Intercept execution events and sync them back to our master database record\n",
    "    if response.function_calls:\n",
    "        print(\"⚙️ [Internal Infrastructure Execution Stack]\")\n",
    "        for call in response.function_calls:\n",
    "            print(f\"  Executed: {call.name}({call.args})\")\n",
    "            if \"city_name\" in call.args:\n",
    "                DATABASE_MOCK[\"session_state\"][\"last_city_searched\"] = call.args[\"city_name\"]\n",
    "                \n",
    "    # If the model gives us back a solid summary containing data, let's keep track of it\n",
    "    if response.text and (\"Temperature:\" in response.text or \"°C\" in response.text):\n",
    "        DATABASE_MOCK[\"session_state\"][\"last_weather_lookup_data\"] = response.text.strip()\n",
    "        \n",
    "    print(f\"\\n🤖 Enterprise Agent: {response.text}\\n\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 4: The Multi-Turn Verification Test\n",
    "Run these blocks sequentially to verify the structural integrity of your enterprise state architecture."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Turn 1: Triggers coordinate mapping and active API call routing\n",
    "interact_with_enterprise_agent(\"What is the weather in Paris right now?\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Turn 2: Sunglasses/Umbrella Context Check\n",
    "# EXPECTED BEHAVIOR: No tool calls executed! It fetches data out of the injected system instruction database context.\n",
    "interact_with_enterprise_agent(\"That sounds pleasant. Should I bring a pair of sunglasses or a heavy jacket for my walk?\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 5: Comparative Memory Test\n",
    "Let's test if the system can cleanly sequence back-to-back location logs and compare state histories."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Registering another city context\n",
    "interact_with_enterprise_agent(\"How about Tokyo?\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Inspecting the database variable directly to prove it survives decoupled from runtime objects\n",
    "import pprint\n",
    "print(\"--- Current Master DB Records ---\")\n",
    "pprint.pprint(DATABASE_MOCK)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

filename = "enterprise_decoupled_agent.ipynb"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print(f"File created successfully: {filename}")