# Dyslexic 🧠  
AI-Powered Literacy & Dyslexia Assistant
> **"Democratizing web accessibility through server-side intelligence."**

**Dyslexic**  is a hybrid browser extension and Python AI backend designed to bridge the gap between standard web content and neurodivergent processing needs. Unlike simple "overlay" extensions that just change fonts, Dyslexic uses **Natural Language Processing (NLP)**, **Stylometric Analysis**, and **Deep Learning** to understand the *context* of text, not just its spelling.

This tool moves beyond simple "overlay" extensions by using server-side natural language processing to understand the *context* of text, not just the ***spelling***. It provides real-time content adaptation, authorship analysis, and multi-modal reading assistance (Text-to-Speech, Dictation, and Visual Overrides).

---

## Key Features & Capabilities

### 1. 👁️ Visual Cognitive Load Management
* **Dyslexia-Friendly Font Overrides:** Instantly reflow web content into **OpenDyslexic**, **Arial**, or **Times New Roman** to reduce visual crowding.
* **Bionic Reading Mode:** Highlights the first few letters of every word to guide the eye and improve reading speed. 
* **Distraction-Free Reader:** Strips ads, sidebars, and navigational clutter, isolating the core text for focused consumption.
* **Dynamic Typography:** Real-time adjustment of font size, line height, and letter spacing to suit individual reading needs.

### 2. 🧠 The "Brain": Stylometric & AI Analysis
* **Complexity Scoring:** Analyzes sentence structure to calculate "Average Sentence Complexity" and "Vocabulary Richness" (Type-Token Ratio).
* **Authorship Attribution:** Uses vector-based distance calculations to compare text against known styles (e.g., distinguishing academic formal vs. blog casual).
    * *Algorithm:* Weighted feature vectors including **Average Word Length**, **Hapax Legomena** (unique word ratio), and **Sentence Phrase Density**.
* **Contextual Re-Ranking (BERT):** Uses Hugging Face Transformers to distinguish between homophones (*their/there/they're*) based on sentence context. 

### 3. 🛡️ Dyslexia Correction Engine
* **Phonetic Hashing:** Converts words to their IPA sound codes (e.g., /kəmˈpjuːtər/) to catch phonetic spelling errors (e.g., "frend" $\rightarrow$ "friend").
* **Visual Distance Weighting:** The algorithm understands that neurodivergent users confuse specific shapes. It prioritizes corrections based on visual similarity (e.g., weighting 'b'/'d' swaps lower than random typos).

### 4. 🗣️ Smart Reading Assistance
* **Contextual Definitions:** Double-click any word to retrieve its definition, part of speech, and usage examples.
* **Phonetic Breakdown:** Displays IPA phonetic spelling (e.g., */kəmˈpjuːtər/*) to aid in decoding. 
* **Integrated Text-to-Speech (TTS):** One-click audio playback using Google's TTS API, allowing users to "read with their ears" without leaving the DOM.

### 5. ✍️ Active Learning & Annotation
* **Smart Dictation:** Speech-to-text input for form fields and essays, powered by backend processing for higher accuracy.
* **Web Annotation:** Highlight text and attach sticky notes/comments directly to the webpage DOM.
* **PDF Intelligence:** Capable of extracting text from browser-rendered PDFs for summarization and commenting (currently in beta).
---

## 🏗️ System Architecture

Dyslexic utilizes a **Hybrid Client-Server Architecture** to overcome browser resource limitations.

### **The Frontend (Firefox Extension)**
* **Stack:** JavaScript (ES6), HTML5, CSS3, WebExtension API.
* **Role:** The "Face". Handles DOM manipulation (font injection), user events (clicks/highlighting), and captures audio.

### **The Backend (Python API)**
* **Stack:** Python 3.10+, Flask, Transformers (BERT), Scikit-learn, TextBlob.
* **Role:** The "Brain". Offloads heavy NLP computations (tokenization, vectorization, sentiment analysis) from the client to the server.

---


## 🛠️ Installation & Setup

### Prerequisite: Python Backend
1.  **Clone the Repo:**
    \`\`\`bash
    git clone https://github.com/AidanColvin/dyslexic.git
    cd dyslexic
    \`\`\`

2.  **Install Dependencies:**
    \`\`\`bash
    # Create virtual environment (Recommended)
    python -m venv venv
    source venv/bin/activate
    
    # Install libraries
    pip install -r requirements.txt
    \`\`\`

3.  **Start the Server:**
    \`\`\`bash
    python run.py
    \`\`\`
    *Output:* \`Running on http://0.0.0.0:5000\`

### Loading the Extension

**Option A: Load from source (for development)**
1.  Open Firefox and navigate to \`about:debugging\`.
2.  Click **"This Firefox"** > **"Load Temporary Add-on"**.
3.  Navigate to the \`extension/\` folder and select \`manifest.json\`.
4.  The Dyslexic icon will appear in your toolbar.

**Option B: Build and install the packaged extension**
1.  Run the build script from the project root:
    \`\`\`bash
    bash build.sh
    \`\`\`
2.  This creates \`dyslexic-firefox.zip\` in the project root.
3.  Open Firefox and navigate to \`about:debugging\`.
4.  Click **"This Firefox"** > **"Load Temporary Add-on"**.
5.  Select the generated \`dyslexic-firefox.zip\` file.

---

## Usage Guide

**1. Reading Mode**
* Click the Dyslexic Icon.
* Toggle "Reader Mode" to strip distractions.
* Select "OpenDyslexic" font and adjust size.

**2. Analyzing Text Complexity**
* Highlight a paragraph.
* Right-click and select **"Analyze Selection with Dyslexic"**.
* View the "Stylometric Signature" (Reading Level & Complexity Score).

**3. Dictionary & Pronunciation**
* Double-click any word.
* A tooltip appears with the definition, IPA phonetics, and a Speaker icon for TTS.

---

## Roadmap
* **v1.1:** Integration of Transformer models (HuggingFace) for context-aware grammar correction. (Completed)
* **v1.2:** "Save to Drive" feature for annotated PDF research papers.
* **v2.0:** Mobile App integration via React Native.

---

## Contributing
Contributions are welcome! Please read \`CONTRIBUTING.md\` for details on our code of conduct and the process for submitting pull requests.

**Author:** Aidan Colvin
**License:** MIT
EOF

---

## 📂 Project Structure

```text
Conductor/
├── backend/                  # The Intelligence Layer
│   ├── app.py                # Flask API Gateway & Entry Point
│   ├── dyslexic_logic.py     # Phonetic Hashing & Visual Distance Algorithms
│   ├── context_engine.py     # BERT Transformer Model for Contextualization
│   ├── structure_analyzer.py # Stylometry, Complexity Scoring & HTML Parsing
│   └── user_profile.py       # Active Learning (User Corrections & Lexicon)
├── extension/                # The Browser Interface (Firefox WebExtension)
│   ├── manifest.json         # Extension Configuration
│   ├── content.js            # DOM Injection (Reader Mode/Fonts)
│   ├── background.js         # API Communication
│   ├── popup.html            # User Interface (Menu)
│   ├── popup.js              # Popup Logic
│   └── icons/                # Extension Icons
├── config/                   # Environment Configurations
│   ├── public_mode.env       # Open Access Settings
│   └── private_mode.env      # Secured/API Key Settings
├── tests/                    # Diagnostic Suite
│   ├── test_dyslexic_logic.py
│   ├── test_api_integration.py
│   └── ...
├── run.py                    # Root Launcher
├── build.sh                  # Firefox Extension Build Script
├── Procfile                  # Cloud Deployment Config (Render/Heroku)
└── requirements.txt          # Python Dependencies
```
---
