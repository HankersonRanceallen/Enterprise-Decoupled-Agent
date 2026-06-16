# Enterprise-Decoupled-Agent

## Enterprise-Grade AI Agent with Stateful Memory & Multi-Step Tool Chaining

A production-oriented AI agent built with the Google GenAI SDK that demonstrates:

* Stateful conversational memory
* Autonomous multi-step tool chaining
* Decoupled persistence architecture
* Cloud API integration
* Resource-efficient reasoning

The project runs in:

* Google Colab
* Jupyter Notebook
* AWS SageMaker
* Local Python environments

---

# Why This Project Matters

Many AI agent tutorials demonstrate basic tool calling but fail enterprise requirements because they suffer from:

### Context Loss

The agent forgets previous interactions and repeatedly requests information.

### Resource Waste

The agent repeatedly calls external APIs for information it already possesses.

### Lack of State Persistence

Conversation context disappears when the runtime session ends.

This project demonstrates solutions to each of these problems.

---

# System Architecture

```text
┌──────────────────────────────────────┐
│              User Input              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│      Database Mock / State Layer     │
│  (Simulates Redis or SQLite Storage) │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Gemini Runtime Layer        │
│                                      │
│  • Conversational Memory             │
│  • Autonomous Tool Routing           │
│  • Multi-Step Reasoning              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│      External Infrastructure         │
│                                      │
│  • Weather APIs                      │
│  • Geocoding Services                │
│  • Future MCP Tools                  │
└──────────────────────────────────────┘
```

---

# Architectural Concepts

## Stateful Memory

The agent maintains conversational history across interactions.

Example:

User:

```text
What's the weather in Paris?
```

Later:

```text
Should I bring sunglasses?
```

The agent remembers the weather context without calling external services again.

---

## Autonomous Tool Chaining

The model can execute multiple tools in sequence.

Example workflow:

```text
City Name
    ↓
search_city_coordinates()
    ↓
Latitude / Longitude
    ↓
get_current_weather()
    ↓
Final Response
```

The user only provides a city name.

The agent determines the remaining execution path automatically.

---

## Decoupled State Management

The project includes a lightweight state repository:

```python
DATABASE_MOCK
```

This simulates production systems such as:

* Redis
* PostgreSQL
* DynamoDB

The pattern allows business state to persist independently of the LLM runtime.

---

# Validation Scenarios

## Umbrella vs Sunglasses Test

```python
interact_with_agent(
    "What's the weather in Paris right now?"
)

interact_with_agent(
    "Would you recommend sunglasses?"
)
```

Expected behavior:

* First prompt triggers tools
* Second prompt uses memory
* No additional API calls

---

## Comparative Memory Test

```python
interact_with_agent("What's the weather in Paris?")
interact_with_agent("How about Tokyo?")
interact_with_agent(
    "Which city is more comfortable for a walk?"
)
```

Expected behavior:

* Agent compares previously collected information
* No additional weather requests required

---

# Technology Stack

| Layer                   | Technology          |
| ----------------------- | ------------------- |
| Foundation Model        | Gemini 2.5 Flash    |
| Agent Runtime           | Google GenAI SDK    |
| Infrastructure API      | Open-Meteo          |
| Development Environment | Jupyter Notebook    |
| State Management        | Mock Database Layer |
| Future Persistence      | Redis / PostgreSQL  |

---

# Installation

## Install Dependencies

```bash
pip install google-genai requests
```

---

## Configure API Key

### Google Colab

Add a secret named:

```text
GEMINI_API_KEY
```

Enable notebook access.

### Local Environment

```bash
export GEMINI_API_KEY="your-key"
```

---

# Running the Agent

Execute the notebook:

```text
enterprise_decoupled_agent.ipynb
```

The notebook is organized into:

1. Dependency Installation
2. Tool Definitions
3. Stateful Agent Initialization
4. Validation Tests

---

# Scalability Roadmap

## State Persistence

Replace:

```python
DATABASE_MOCK
```

With:

* Redis
* PostgreSQL

---

## Deterministic Agent Routing

Move from free-form tool calling to:

* LangGraph
* State Machines
* Enterprise Workflow Graphs

---

## Evaluation Frameworks

Integrate:

* RAGAS
* TruLens
* Custom Benchmark Pipelines

To validate future prompt and model updates.

---

# Future Improvements

* Long-term memory storage
* Redis-backed conversation persistence
* Multi-user sessions
* MCP tool integration
* LangGraph orchestration
* Production API deployment
* Monitoring and observability

---
