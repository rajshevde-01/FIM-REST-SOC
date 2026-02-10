# FIM-REST-SOC
File &amp; Windows Registry Integrity Monitoring System (Web + Agent)  A REST-based File Integrity Monitoring (FIM) solution with agent–server architecture, real-time alerts, Windows Registry monitoring, MITRE ATT&amp;CK mapping, and a web dashboard — designed from a Blue Team / SOC Analyst perspective.
🚀 Project Overview

FIM-REST continuously monitors:

📁 Critical files & directories

🪟 Windows Registry persistence locations

🔐 Unauthorized changes, deletions, or creations

All events are:

Hash-verified (SHA-256)

Sent to a central REST API

Logged and visualized on a web dashboard

Mapped to MITRE ATT&CK techniques

This simulates how enterprise FIM tools (Tripwire, Wazuh, OSSEC) operate in real SOC environments.

🧠 Why This Tool Exists (Purpose)

Attackers often:

Modify system files

Add registry persistence keys

Deface web files

Evade detection by avoiding malware drops

👉 File & Registry Integrity Monitoring detects these stealthy attacks early, even when no malware is present.

This tool demonstrates defensive detection, not offensive exploitation.

🧱 Architecture
           ┌────────────┐
           │  FIM Agent │
           │ (Windows)  │
           └─────┬──────┘
                 │ REST API (JSON alerts)
                 ▼
        ┌───────────────────┐
        │   Flask Server     │
        │  Alert Processing │
        └─────┬─────────────┘
              │
              ▼
     ┌─────────────────────┐
     │ Web Dashboard (UI)  │
     │ SQLite Alert Store  │
     └─────────────────────┘

✨ Key Features
🔍 File Integrity Monitoring

Detects:

File creation

File modification

File deletion

Uses SHA-256 hashing

Baseline vs drift detection

🪟 Windows Registry Monitoring (Advanced)

Monitors persistence-related registry keys:

HKCU\Software\Microsoft\Windows\CurrentVersion\Run

RunOnce

Detects:

Registry value creation

Registry modification

Registry deletion

Mapped to:

MITRE ATT&CK T1547 – Boot or Logon Autostart Execution

🚨 Real-Time Alerts

CLI alerts on agent

REST alerts to server

Stored centrally

Viewable in web dashboard

🧠 MITRE ATT&CK Mapping

Each alert is mapped to tactics & techniques:

Detection	MITRE Technique
Registry persistence	T1547
System file change	T1548
Web file modification	T1491
File discovery	T1083
🌐 Web Dashboard

SOC-style alert table

Severity classification

Timeline view

Centralized visibility

📁 Project Structure
FIM-REST/
│
├── agent/
│   ├── agent.py              # Main FIM agent
│   ├── config.py             # Agent configuration
│   ├── hasher.py             # SHA-256 hashing
│   ├── monitor.py            # File monitoring
│   └── registry_monitor.py   # Windows Registry FIM
│
├── monitored/
│   └── test.txt              # Sample monitored file
│
└── server/
    ├── app.py                # Flask REST API + dashboard
    ├── database.db           # SQLite alert database
    ├── requirements.txt
    ├── static/style.css
    └── templates/dashboard.html

⚙️ Installation & Setup
🔹 Requirements

Python 3.9+

Windows OS (for registry monitoring)

Flask

🔹 Clone Repository
git clone https://github.com/yourusername/FIM-REST.git
cd FIM-REST

🔹 Setup Server
cd server
pip install -r requirements.txt
python app.py


Open dashboard:

http://127.0.0.1:5000

🔹 Setup Agent
cd agent
python agent.py

🧪 Testing the Tool
✅ File Change Test
echo "attack simulation" >> monitored/test.txt


Expected output:

[FILE ALERT] MODIFIED → ../monitored/test.txt

✅ Registry Persistence Test (PowerShell)
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run `
/v EvilTest /t REG_SZ /d evil.exe


Expected:

[REG ALERT] CREATED → HKCU\...\Run\EvilTest


Dashboard updates instantly.

🚨 Alert Example (JSON)
{
  "agent_id": "agent-01",
  "file": "HKCU\\...\\Run\\EvilTest",
  "change": "REG_CREATED",
  "severity": "HIGH",
  "mitre": "T1547",
  "timestamp": "2026-02-10T10:32:11"
}

🧑‍💻 SOC Analyst Skills Demonstrated

File Integrity Monitoring (FIM)

Endpoint detection logic

Windows persistence detection

MITRE ATT&CK mapping

Agent-server architecture

REST API design

Alert triage concepts

Blue Team defensive mindset

🔮 Future Enhancements

Email / Slack alerts

Windows Services monitoring

Scheduled Task FIM

ELK / Splunk integration

API key–based agent authentication

Dockerized deployment

⚠️ Disclaimer

This project is for educational and defensive security purposes only.
Do not deploy in production without hardening, authentication, and access controls.

⭐ If You Like This Project

Give it a ⭐ on GitHub — it helps a lot and shows appreciation!
