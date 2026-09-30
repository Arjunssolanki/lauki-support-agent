# MESS-RAG Voice Assistant Pipeline 🎙️

An enterprise-ready, fully open-source and free **Conversational Voice AI Agent Platform** powered by local Vector Retrieval-Augmented Generation (RAG) architecture and high-speed cloud inference engines. This pipeline ingests messy corporate knowledge documents (PDFs and Microsoft Word `.docx` layouts), transforms them into semantic high-dimensional vector embeddings, and enables a hands-free conversational voice loop leveraging active Bluetooth headsets for sub-second support routing.

---

## 🏛️ Comprehensive Project Architecture & Data Flow

The system operates like an isolated, event-driven smart processing data pipeline where audio, text, and vector stores interact dynamically:

```text
 [Messy Documents] (.pdf, .docx)
         │
         ▼ (ingest.py via pypdf / python-docx)
 [Recursive Text Chunking]
         │
         ▼ (Local onnx model: all-MiniLM-L6-v2)
 [ChromaDB Vector Store] (Persistent Storage)
         │
         ├─── Query Context Ingestion ───┐
         ▼                               ▼
 [Speech Capture Loop] (agent.py) ──► [Groq Cloud Inference] (qwen/qwen3.8-27b)
   Microphone (Noise Aura Buds)          │ (Sub-second text synthesis)
                                         ▼
 [Audio Output System] ◄────────────── [gTTS & Pygame Engine]
   Speaker Broadcast & Log Storage
```

---

## 🛠️ Infrastructure & Setup Summary

### 1. Compute & Local Storage Engine

- **Workspace OS Matrix:** Windows Native Host Pipeline.
- **Vector Base Database Engine:** ChromaDB Local Persistent Engine utilizing standard `all-MiniLM-L6-v2` ONNX models natively down to local user cache directories.
- **Inference Acceleration:** Groq API Cloud Architecture utilizing the specialized, high-capacity, sub-second `qwen/qwen3.8-27b` inference processor tier.

### 2. Audio Pipeline Layer

- **Speech-to-Text (STT):** `SpeechRecognition` client abstraction routing locally captured binaries out to Google Web Speech API interfaces.
- **Text-to-Speech (TTS):** `gTTS` (Google Text-To-Speech) compiler coupled with `pygame.mixer` threads for low-overhead audio wave broadcasting.
- **Hardware Profile Mapping:** Fixed mono communication stream locked to standard Windows Audio Endpoint Indexes running channel boundaries natively at **8000 Hz / 16000 Hz** tracking limits.

---

## 💻 Workspace Configuration (Windows Client)

All local project management operations are executed from the active target directory:
`D:\2026\newstudy\projects\lauki-support-agent>`

### 1. Isolated Workspace Runtime Environment

The project runs within an isolated virtual workspace to prevent cross-contamination of system libraries:

```powershell
# Create the local python virtual environment path natively
python -m venv venv

# Activate the localized platform runtime environment shell workspace
venv\Scripts\activate.ps1
```

### 2. Core Framework Dependency Stack

All dependencies are cleanly managed without hardcoded version strings to maintain deployment scalability:

```powershell
pip install -r requirements.txt
```

---

## 🔌 Repository Manifest & Core Logical Components

### 1. Environment Manager Configuration (`.env`)

Houses critical API credentials and directory configuration matrices isolated from global version control trees:

- `GROQ_API_KEY`: Secure cloud token string.
- `GROQ_MODEL`: Active high-speed inference string set to `qwen/qwen3.8-27b`.
- `VECTOR_DB_PATH`: Persistent data mapping string (`./chroma_db`).

### 2. Automated Multimodal Schema Ingestion Engine (`ingest.py`)

Parses, cleans, and indexes multi-format documents across the internet or local directories into ChromaDB:

- **PDF Extraction Module:** Iterates structural layout sheets via `pypdf`, tracking page numbers.
- **Word Document Module:** Parses paragraph fragments and table rows (`python-docx`), combining cell values with pipe delimiters (`|`) for advanced layout retention.
- **Chunking Stratagem:** Groups text block metrics using dual line breakers (`\n\n`) to guard semantic boundary thresholds.

### 3. Verification & Diagnostic Engine (`test_brain.py`)

Executes standalone semantic sanity validations by searching the local database, constructing advanced system wrappers, and analyzing the response times of the Groq cloud controller.

### 4. Interactive Voice Assistant Controller Loop (`agent.py`)

The primary execution script controlling microphone inputs, semantic searching, API routing, and speaker playback.

- **Device Anchoring:** Targets high-level Bluetooth audio channels (e.g., _Noise Aura Buds_) using exclusive capture hooks.
- **Audio Logging System:** Diverts operational speech waves right before local buffer purges, saving permanent timestamped voice logs (`.mp3`) inside `./saved_audio/` for auditable tracking.

---

## 📊 Business Insights Discovery & Testing Guidelines

Run the vector indexing script to process manual files:

```bash
python ingest.py
```

Fire up the interactive voice platform:

```bash
python agent.py
```

### Verified Test Queries:

- **Plans & Pricing:** _"What are the available billing plans?"_
- **Account Operations:** _"How can I check my current outstanding bill?"_
- **Network Boundaries:** _"Tell me about network coverage availability."_
- **Out-of-Bounds Rejection:** _"Explain how to fix a broken car tire."_ (The agent will accurately refuse to answer based on system prompt bounds).
