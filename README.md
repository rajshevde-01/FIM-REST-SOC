# FIM-REST-SOC
File & Windows Registry Integrity Monitoring System (Web + Agent)

A REST-based File Integrity Monitoring (FIM) solution with agent-server architecture, real-time alerts, Windows Registry monitoring, MITRE ATT&CK mapping, and a web dashboard built for Blue Team / SOC workflows.


## Overview
FIM-REST monitors:

- Critical files and directories
- Windows Registry persistence locations
- Unauthorized creations, modifications, and deletions

All events are:

- Hash-verified (SHA-256)
- Sent to a central REST API
- Stored in SQLite
- Visualized in a web dashboard
- Mapped to MITRE ATT&CK techniques

### Architecture
+------------+         REST JSON          +------------------+        SQLite        +---------------------+
|  FIM Agent |  ----------------------->  |   Flask Server   |  ----------------->   | Web Dashboard (UI)  |
| (Windows)  |                             |  Alert Handling  |                      | Alerts and MITRE    |
+------------+                             +------------------+                      +---------------------+

## Components
### Agent
- File integrity monitoring (create/modify/delete)
- Registry monitoring for persistence keys
- REST alert emission (JSON)

### Server
- Receives alerts via REST API
- Persists alerts in SQLite
- Adds severity and MITRE mappings

### Dashboard
- SOC-style alert table
- Severity indicators
- Timeline view

## Key Features
### File Integrity Monitoring
- Baseline hashing with SHA-256
- Drift detection for modifications
- Creation and deletion tracking

### Windows Registry Monitoring
Monitors persistence-related keys:

- HKCU\Software\Microsoft\Windows\CurrentVersion\Run
- RunOnce

Detects:

- Registry value creation
- Registry value modification
- Registry value deletion

Maps to:

- MITRE ATT&CK T1547 (Boot or Logon Autostart Execution)

### MITRE ATT&CK Mapping
| Detection             | MITRE Technique |
|-----------------------|-----------------|
| Registry persistence  | T1547           |
| System file change    | T1548           |
| Web file modification | T1491           |
| File discovery        | T1083           |

### Repository Structure
FIM-REST/
|-- agent/
|   |-- agent.py
|   |-- config.py
|   |-- hasher.py
|   |-- monitor.py
|   `-- registry_monitor.py
|-- monitored/
|   `-- test.txt
`-- server/
    |-- app.py
    |-- requirements.txt
    |-- static/
    |   `-- style.css
    `-- templates/
        `-- dashboard.html

## Installation and Setup
### Requirements
- Python 3.9+
- Windows OS (for registry monitoring)
- Flask

### Clone Repository
```
git clone https://github.com/rajshevde-01/FIM-REST-SOC.git
cd FIM-REST
```

### Start Server
```
cd server
pip install -r requirements.txt
python app.py
```

Dashboard:

http://127.0.0.1:5000

### Start Agent
```
cd agent
python agent.py
```

## Testing
### File Change Test
```
echo "attack simulation" >> monitored/test.txt
```

Expected:

```
[FILE ALERT] MODIFIED -> ../monitored/test.txt
```

### Registry Persistence Test (PowerShell)
```
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run `
/v EvilTest /t REG_SZ /d evil.exe
```

Expected:

```
[REG ALERT] CREATED -> HKCU\...\Run\EvilTest
```

## Alert Example (JSON)
```
{
  "agent_id": "agent-01",
  "file": "HKCU\\...\\Run\\EvilTest",
  "change": "REG_CREATED",
  "severity": "HIGH",
  "mitre": "T1547",
  "timestamp": "2026-02-10T10:32:11"
}
```

## Skills Demonstrated
- File integrity monitoring (FIM)
- Endpoint detection logic
- Windows persistence detection
- MITRE ATT&CK mapping
- Agent-server architecture
- REST API design
- Alert triage concepts

## Roadmap
- Email or Slack alerts
- Windows Services monitoring
- Scheduled Task FIM
- ELK or Splunk integration
- API key-based agent authentication
- Dockerized deployment

## Disclaimer
This project is for educational and defensive security purposes only.
Do not deploy in production without hardening, authentication, and access controls.
