# Fahamika

Built during the Democracy & AI Hackathon — July 4th, 2026
Hosted by Mozilla Foundation & KamiLimu

## Team

| Name | Role | GitHub |
|------|------|--------|
| Christine Mugo | Data Scientist | @mugochristine25-coder |
| Jenas Jermaine | Data Scientist | @JenasJermaine |

**Team Name:** TO13-J-C
**University:** USIU(Christine) and University of Nairobi (Jermaine)

## Problem & User

### Problem Statement
Persons with disabilities (PWDs) in Kenya face significant barriers accessing information about their legal rights. Official civic content is published as lengthy, technical English documents on government websites — requiring a smartphone, stable internet, and high literacy levels. For citizens in areas with limited connectivity, or those who are visually or hearing impaired, this creates a near-total information blackout on fundamental rights they are entitled to under Kenyan law.

### Target User

| Dimension | Detail |
|-----------|--------|
| Primary user | A PWD in a rural or peri-urban area with limited smartphone access |
| Tech comfort | Comfortable with a basic feature phone; may not own a smartphone |
| Language |English, Swahili, Sheng, vernacular languages |
| Current workflow | Learns about rights through word-of-mouth, local radio, or community barazas — no way to verify or access the full text independently |

### The Specific Gap

**What's already there:** Kenya's Persons with Disabilities Act and related civic content exists in government archives and NGO publications.

**Why it falls short:** Published as dense English PDFs; require a desktop browser or smartphone, stable internet, and advanced literacy. No phone-based, voice-first access path exists.

**The gap we fill:** A toll-free phone service that reads approved civic information aloud in plain Swahili or English — accessible from any feature phone, no internet required. The AI simplifies the language but never invents facts; all content is sourced from a pre-approved database.

### Why It Matters
When citizens with disabilities cannot access their own rights, the legal protections written on paper mean nothing in practice. A person who doesn't know they have the right to own property, access credit, or be free from discrimination is a person who cannot exercise those rights. An IVR-based phone line — the most universal communication channel available — closes the gap between a right that exists on paper and a right a citizen can actually use.

## Run Instructions

### Prerequisites
- Ubuntu 24 VM (VirtualBox with bridged network adapter)
- Windows host with Ollama installed
- Python 3.10+
- Asterisk (PBX)
- Zoiper (or any SIP softphone for testing)

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/[org]/[repo].git
cd [repo]

# 2. Install system dependencies (Ubuntu VM)
sudo apt update
sudo apt install asterisk sox python3-venv -y

# 3. Create a virtual environment
sudo python3 -m venv /opt/civic/venv
sudo /opt/civic/venv/bin/pip install -r requirements.txt

# 4. Set up Firebase credentials
#    Download serviceAccountKey.json from Firebase Console
#    Place it at /opt/civic/serviceAccountKey.json
sudo chown -R asterisk:asterisk /opt/civic

# 5. Download Piper voice model
sudo -u asterisk bash -c "cd /opt/civic && /opt/civic/venv/bin/python3 -m piper.download_voices --data-dir /opt/civic/voices en_US-lessac-medium"

# 6. Deploy Asterisk configs
sudo cp src/configuration/pjsip.conf /etc/asterisk/pjsip.conf
sudo cp src/configuration/extensions.conf /etc/asterisk/extensions.conf
sudo asterisk -rx "pjsip reload"
sudo asterisk -rx "dialplan reload"

# 7. Deploy scripts
sudo cp src/scripts/*.py /opt/civic/
sudo chown asterisk:asterisk /opt/civic/*.py
sudo mkdir -p /opt/civic/recordings /opt/civic/whisper_models
sudo chown -R asterisk:asterisk /opt/civic/recordings /opt/civic/whisper_models

# 8. Update Windows host IP in the scripts
#    Replace <WINDOWS_LAN_IP> in fetch_and_speak.py and transcribe_and_speak.py

# 9. Register Zoiper to the VM's IP (extension 6001 / changeme123) and dial 200
```

For full setup details, see [SETUP.md](SETUP.md).

## Project Structure

```
.
├── README.md
├── SETUP.md                              ← Full setup guide for VM + Windows host
├── requirements.txt                      ← Python + system dependency listing
├── .gitignore
├── LICENSE
│
├── docs/
│   ├── problem-statement.md              ← Detailed problem breakdown
│   ├── PWD_Connectivity_Buildathon_Build_Log.docx  ← Prep-day build log
│   ├── architecture.png                  ← System architecture diagram
│   └── configs/                          ← Asterisk reference configs
│       ├── extensions.conf               ← Dialplan (extensions 100 & 200)
│       └── pjsip.conf                    ← SIP endpoint (6001)
│
├── src/
│   ├── scripts/                          ← Python pipeline scripts
│   │   ├── fetch_and_speak.py            ← Fixed-topic IVR pipeline (dial 100)
│   │   └── transcribe_and_speak.py       ← Voice-input pipeline (dial 200)
│   └── configuration/                    ← Copies for deployment
│       ├── extensions.conf
│       └── pjsip.conf
│
└── data/
    └── civic_content_sample.json         ← Sample Firestore document (disability_rights)
```

## Approach & Architecture

```
 Feature phone / SIP softphone (Zoiper)
        │
        ▼
 Asterisk PBX (Ubuntu VM, bridged network)
        │  System() call spawns a Python script
        ▼
 Firebase Firestore ─── fetch approved civic_content document
        │
        ▼
 Ollama (Windows host, llama3.2:1b) ─── simplify / translate text
        │
        ▼
 Piper (neural TTS) ─── generate speech audio
        │
        ▼
 sox ─── resample audio to 8 kHz mono (telephony format)
        │
        ▼
 Asterisk Playback() ─── caller hears the response
```

**Extension 100:** Fixed-topic pipeline — dial, hear simplified civic rights read aloud.
**Extension 200:** Voice-input pipeline — speak a question, get transcribed via faster-whisper, matched to a topic, and read back.

The AI model (Ollama with llama3.2:1b) only rewrites and translates pre-approved text from Firestore. It never generates civic information from its own knowledge — keeping the system's factual content controlled, auditable, and safe for a civic-accountability use case.

## License

MIT © [Team Name], 2026
