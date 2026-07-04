import sys, subprocess, requests
import firebase_admin
from firebase_admin import credentials, firestore

topic = sys.argv[1] if len(sys.argv) > 1 else "disability_rights"
lang = sys.argv[2] if len(sys.argv) > 2 else "en"

cred = credentials.Certificate("/opt/civic/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

doc = db.collection("civic_content").document(topic).get()
text = doc.to_dict().get(f"body_{lang}", "Content not found")

resp = requests.post("http://192.168.2.110:11434/api/generate", json={
    "model": "llama3.2:1b",
    "prompt": f"Rewrite this in very simple {lang}, under 50 words, no new facts: {text}",
    "stream": False
})
simple_text = resp.json().get("response", text)

with open("/tmp/say.txt", "w") as f:
    f.write(simple_text)

subprocess.run(
    ["/opt/civic/venv/bin/piper", "--model", "en_US-lessac-medium",
     "--data-dir", "/opt/civic/voices", "--output_file", "/tmp/raw.wav"],
    input=simple_text, text=True, cwd="/opt/civic"
)
subprocess.run(["sox", "/tmp/raw.wav", "-r", "8000", "-c", "1", "/opt/civic/output.wav"])
