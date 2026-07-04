Setup Guide

## Prerequisites

- Ubuntu 24 VM (VirtualBox, bridged network adapter)
- Windows host with Ollama installed
- Python 3.10+

## 1. System Packages

```bash
sudo apt update
sudo apt install asterisk sox python3-venv -y
sudo systemctl start asterisk
sudo systemctl enable asterisk
```

## 2. Python Environment

```bash
sudo python3 -m venv /opt/civic/venv
sudo /opt/civic/venv/bin/pip install -r requirements.txt
sudo chown -R asterisk:asterisk /opt/civic
```

## 3. Firebase Service Account

1. Go to Firebase Console → Project Settings → Service Accounts
2. Generate new private key
3. Save to `/opt/civic/serviceAccountKey.json`
4. `sudo chown asterisk:asterisk /opt/civic/serviceAccountKey.json`

## 4. Piper Voice Model

```bash
sudo -u asterisk bash -c "cd /opt/civic && /opt/civic/venv/bin/python3 -m piper.download_voices --data-dir /opt/civic/voices en_US-lessac-medium"
```

## 5. Whisper Model

Downloaded automatically on first use by `faster-whisper`. Set a HuggingFace token to speed it up:

```bash
sudo mkdir -p /etc/systemd/system/asterisk.service.d
sudo tee /etc/systemd/system/asterisk.service.d/hf_token.conf << 'EOF'
[Service]
Environment="HF_TOKEN=hf_your_token_here"
EOF
sudo systemctl daemon-reload
sudo systemctl restart asterisk
```

## 6. Ollama (Windows Host)

```powershell
ollama pull llama3.2:1b
# Set environment variable: OLLAMA_HOST=0.0.0.0:11434
# Allow through firewall:
#   New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow
```

## 7. Asterisk Configuration

Copy the configs from `src/configuration/` to the VM:

```bash
sudo cp src/configuration/pjsip.conf /etc/asterisk/pjsip.conf
sudo cp src/configuration/extensions.conf /etc/asterisk/extensions.conf
sudo asterisk -rx "pjsip reload"
sudo asterisk -rx "dialplan reload"
```

## 8. Deploy Scripts

```bash
sudo cp src/scripts/*.py /opt/civic/
sudo chown asterisk:asterisk /opt/civic/*.py
sudo mkdir -p /opt/civic/recordings
sudo chown -R asterisk:asterisk /opt/civic/recordings
```

Replace `<WINDOWS_LAN_IP>` in both scripts with your Windows host's bridged IP.

## 9. Verify

```bash
# Test Ollama connectivity
sudo -u asterisk curl http://<WINDOWS_LAN_IP>:11434/api/tags

# Test the pipeline
sudo -u asterisk /opt/civic/venv/bin/python3 /opt/civic/fetch_and_speak.py disability_rights en
echo $?   # should be 0

# Register Zoiper to the VM's IP (extension 6001 / changeme123) and dial 100
```

## File Placement on VM

```
/opt/civic/
├── venv/
├── serviceAccountKey.json   ← NOT in repo, from Firebase
├── voices/                  ← NOT in repo, downloaded
├── whisper_models/          ← NOT in repo, downloaded on first use
├── recordings/              ← created at runtime
├── fetch_and_speak.py
├── transcribe_and_speak.py
├── output.wav               ← generated at runtime
└── transcribe_log.txt       ← generated at runtime
```
