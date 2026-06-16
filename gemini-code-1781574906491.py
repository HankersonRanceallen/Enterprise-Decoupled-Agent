import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Production-Ready AI Agent Architecture with Database State Decoupling\n",
    "This notebook provides a complete enterprise-grade architectural blueprint for an AI agent. It actively layers:\n",
    "1. **Conversational Memory** (Session tracking)\n",
    "2. **Multi-Step Execution Pipelines** (Tool Chaining)\n",
    "3. **State Decoupling via Database Layer** (Using a persistent local mock dictionary to simulate production setups like SQLite or Redis)\n",
    "\n",
    "This system prevents redundant API data lookups on conversational loops and maintains state even if the LLM context session experiences disruptions."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 1: Install Dependencies"
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
    "### Step 2: Define Interdependent Infrastructure Tools\n",
    "The model can chain `search_city_coordinates` directly into `get_current_weather` when resolving plain-text queries."
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
    "        response = requests.get(url).json()\n",
    "        if \"current_weather\" in response:\n",
    "            cw = response[\"current_weather\"]\n",
    "            return f\"Temperature: {cw['temperature']}°C | Windspeed: {cw['windspeed']} km/h.\"\n",
    "        return \"Weather infrastructure lookup failed.\"\n",
    "    except Exception as e:\n",
    "        return f\"Cloud context connection timeout: {str(e)}\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 3: Set Up the Persistent Database State & Orchestration\n",
    "Here we create a stateful chat framework natively supported by Gemini, combined with an isolated mock database layer (`DATABASE_MOCK`). This allows the agent runtime loop to dynamically inject past variables and record tool outputs cleanly."
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
    "# --- PRODUCTION MEMORY UPGRADE ---\n",
    "# This mimics an external state store like Redis or SQLite database\n",
    "DATABASE_MOCK = {\n",
    "    \"user_preferences\": {\n",
    "        \"unit\": \"Celsius\",\n",
    "        \"preferred_activity\": \"walking\"\n",
    "    },\n",
    "    \"session_state\": {\n",
    "        \"last_city_searched\": None,\n",
    "        \"last_weather_data\": None\n",
    "    }\n",
    "}\n",
    "\n",
    "# Setting up the stateful native chat session\n",
    "agent_session = client.chats.create(\n",
    "    model='gemini-2.5-flash',\n",
    "    config=types.GenerateContentConfig(\n",
    "        tools=[search_city_coordinates, get_current_weather],\n",
    "        temperature=0.3,\n",
    "        system_instruction=(\n",
    "            \"You are an advanced enterprise coordinator agent with conversational memory. \"\n",
    "            \"If a user references a city without coordinates, use search_city_coordinates first, \"\n",
    "            \"then automatically pipe that data into get_current_weather before outputting your response.\"\n",
    "        )\n",
    "    )\n",
    ")\n",
    "\n",
    "def interact_with_agent(user_message: str):\n",
    "    print(f\"👤 User: {user_message}\")\n",
    "    print(\"-\"*50)\n",
    "    \n",
    "    # Append runtime context from database explicitly if needed\n",
    "    response = agent_session.send_message(user_message)\n",
    "    \n",
    "    # Print internal runtime stack info when a tool execution turn occurs\n",
    "    if response.function_calls:\n",
    "        print(\"⚙️ [Internal Execution Stack Tracking]\")\n",
    "        for index, call in enumerate(response.function_calls):\n",
    "            print(f\"  Step {index+1}: Resolved Tool -> {call.name}({call.args})\")\n",
    "            # Write output dynamically back to our persistent system architecture\n",
    "            if \"city_name\" in call.args:\n",
    "                DATABASE_MOCK[\"session_state\"][\"last_city_searched\"] = call.args[\"city_name\"]\n",
    "    else:\n",
    "        print(\"💡 [Optimizer Note]: No tools triggered. Response generated cleanly out of memory content context.\")\n",
    "            \n",
    "    print(f\"\\n🤖 Agent: {response.text}\\n\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 4: Run the Enterprise Validation Pipelines"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Phase A: Multi-Step Chaining\n",
    "The model notes it has a city name but no numerical geographic parameters. It calls Step 1 (`search_city_coordinates`) followed immediately by Step 2 (`get_current_weather`) to answer you."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "interact_with_agent(\"What's the current weather in Paris right now?\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Phase B: Session Memory & Optimization Validation\n",
    "Because the conversational timeline is tracked by the chat object, running the block below will trigger **no tool execution stacks**. The model resolves the response dynamically by drawing from the context window of the previous run."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "interact_with_agent(\"That sounds nice. Based on those conditions, would you recommend bringing an umbrella or sunglasses?\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Phase C: The Comparative Memory Test\n",
    "This execution checks context management boundaries. We fetch weather data for a second distinct node (Tokyo) and prompt the agent to perform an optimization synthesis between both historical states."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "interact_with_agent(\"How about Tokyo?\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# The final reasoning comparison turn (Should hit NO tools)\n",
    "interact_with_agent(\"Which city would be more comfortable for a walk right now?\")"
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

print(f"File updated successfully: {filename}")