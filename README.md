# Enterprise-Decoupled-Agent
🚀 Enterprise-Grade AI Agent: Stateful Memory & Multi-Step Tool ChainingA production-adjacent, lightweight AI Agent built using the native Google GenAI SDK and ready to run out-of-the-box in a Jupyter Notebook (Google Colab, AWS SageMaker, or local workspace).This project moves beyond simple "stateless LLM prompts" to demonstrate three core principles of enterprise AI engineering: State Stateful Conversational Memory, Autonomous Multi-Step Tool Chaining, and Database-Layer Decoupling for resource optimization.💡 System Architecture & The "Production Gap"Most beginner AI agent tutorials showcase basic tool usage but fail standard enterprise validation because they suffer from Amnesia (forgetting context across turns) or Resource Inefficiency (making redundant, expensive API calls for information they were already handed).This architecture implements a decoupled approach to fix these limitations:     

                  ┌──────────────────────────────────────────────┐
                  │                 USER INPUT                   │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │       DATABASE MOCK / RESILIENT STATE        │
                  │   (Simulating external SQLite/Redis layer)   │
                  └──────────────────────┬───────────────────────┘
                                         │ Injection of State
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           GEMINI RUNTIME LAYER (LLM)                            │
│                                                                                 │
│   🧠 Context History Window           ⚙️ Internal Autonomous Routing           │
│   (Maintains Turn-by-Turn Memory)      (Chains Search ──> Climate Metrics)      │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │        INFRASTRUCTURE / CLOUD TOOLS          │
                  │     (Executes APIs *only* when needed)       │
                  └──────────────────────────────────────────────┘

                  
Key Architectural Validations Demonstrated:The Umbrella/Sunglasses Test: The agent retains conversational history natively. If asked about what to wear based on a previous weather tool execution, it draws from its internal context window rather than re-triggering the external API—saving compute power and avoiding rate limits.The Comparative Memory Test: The agent can manage multiple data nodes over a timeline (e.g., pulling metrics for Paris, then Tokyo) and perform cross-context comparative analysis natively without invoking any additional tool overhead.Decoupled System State: Implements a localized DATABASE_MOCK memory repository tracking transaction entities (last_city_searched), mimicking how an industrial microservice syncs with a Redis cache or an SQLite instance to ensure persistence beyond runtime engine lifecycles.🛠️ Tech Stack & ServicesCore Runtime Model: gemini-2.5-flashAgent Engine: Google GenAI Python SDK (google-genai)Infrastructure Interface: Open-Meteo Cloud System API (Keyless Geocoding & Climate Engine)Development Workspace: Jupyter Notebook / IPython Pipeline🚀 Getting Started (Notebook Setup)1. InstallationRun the following block inside your notebook to pull down dependencies:Bashpip install google-genai requests
2. Environment VerificationEnsure your model endpoint is authenticated. If running in Google Colab, navigate to the "Secrets" (key icon) tab on the left panel, add a secret named GEMINI_API_KEY, and enable Notebook access.3. Execution Execution FlowsOpen and run enterprise_decoupled_agent.ipynb. The runtime script is broken down into four digestible stages:  Dependency MountsInfrastructure Tool Definitions (Mapping type hints and functional docstrings for model compilation)Persistent Session Context Init (Spinning up stateful routing loops)Validation Test Stack🔬 Validation Tests (What to Look For)When you run the execution stack, observe the standard terminal output closely:Phase A: Autonomous Multi-Step ChainingPythoninteract_with_agent("What's the current weather in Paris right now?")
Expected Output: You will see the ⚙️ [Internal Execution Stack Tracking] fire off two distinct steps in succession. The model realizes it has a text string, translates it to geographic parameters via search_city_coordinates, and pipes those variables smoothly into get_current_weather.  Phase B: Context-Window OptimizationPythoninteract_with_agent("That sounds nice. Based on those conditions, would you recommend bringing an umbrella or sunglasses?")
Expected Output: You will see a 💡 [Optimizer Note]: No tools triggered indicator. The agent successfully avoids hitting external infrastructure because it retains the relative state within its context parameters.  Phase C: Cross-Timeline Context SynthesisPythoninteract_with_agent("How about Tokyo?")
interact_with_agent("Which city would be more comfortable for a walk right now?")
Expected Output: The final prompt invokes zero external function architectures. The system synthesizes the historical state of Turn 1 (Paris) and Turn 3 (Tokyo) out of conversational history to deliver an intelligent, comparative verdict.  📈 Scalability Roadmap to Enterprise ProductionTo transition this portfolio project into a fully distributed microservice architecture, replace the notebook primitives with the following systems:State Persistence Layer: Replace the file's internal DATABASE_MOCK with Redis (for high-velocity session storage caching) or PostgreSQL (for durable chat message history tracking).Deterministic Routing Constraints: For strict business compliance paths, map the raw function tools into an orchestration graph framework like LangGraph, converting model guessing loops into rigid, verifiable state-machines.Enterprise Evaluation Pipelines: Implement testing harnesses (such as Ragas or TruLens) against historical evaluation logs to ensure prompt tweaks don't cause agent accuracy regressions across production endpoints.
