Bien sûr. Voici une version propre, directement copiable dans README.md, avec une présentation GitHub plus professionnelle.

🛡️ Windows Registry Monitor

A lightweight Windows Registry security monitoring tool designed to detect suspicious changes to sensitive Registry keys and identify potential persistence activity.

Built with Python for defensive security monitoring and SOC Analyst training.

---

✨ Features

- 🔍 Monitor sensitive Windows Registry keys
- 🚨 Detect newly created Registry values
- ✏️ Detect modified Registry values
- 🗑️ Detect deleted Registry values
- 🎯 Calculate a risk score from "0–100"
- 🟢 "LOW" risk detection
- 🟡 "MEDIUM" risk detection
- 🟠 "HIGH" risk detection
- 🔴 "CRITICAL" risk detection
- ⚡ Detect executable and script references
- 💻 Detect PowerShell execution
- 🖥️ Detect command interpreters
- 📂 Detect suspicious user-writable locations
- 🔐 Detect basic command obfuscation indicators
- 📟 Real-time terminal alerts

---

🎯 Purpose

Attackers and malware can modify Windows Registry keys to establish persistence and automatically execute programs when a user logs in.

This project monitors common Registry persistence locations and analyzes changes to help identify potentially malicious activity.

---

📌 Monitored Registry Keys

The current version monitors:

HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce

HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce

These Registry locations are commonly associated with Windows startup persistence.

---

🏗️ Project Structure

windows-registry-monitor/
│
├── main.py
├── registry_monitor.py
├── detector.py
├── requirements.txt
├── README.md
│
└── logs/
    └── registry_alerts.log

---

⚙️ Requirements

- Windows 10 / 11
- Python 3.9+
- Administrator privileges may be required for some "HKLM" operations.

Dependencies

The current version uses Python's standard library.

No external packages are required.

---

🚀 Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/windows-registry-monitor.git

2. Enter the project directory

cd windows-registry-monitor

3. Run the monitor

python main.py

---

🖥️ Example

When the program starts:

============================================================
 Windows Registry Monitor
============================================================

When a suspicious Registry modification is detected:

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[ALERT] Risk: HIGH
Score : 75/100
Action: VALUE_CREATED
Key   : Software\Microsoft\Windows\CurrentVersion\Run
Value : updater
Data  : C:\Users\User\AppData\Roaming\updater.exe

Reasons:
  - Registry persistence location
  - New registry value created
  - Executable or script referenced
  - User-writable or temporary location
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---

🧠 Detection Engine

The detection engine analyzes several indicators.

Indicator| Score
Registry persistence location| +30
New Registry value| +20
Executable / script reference| +20
Suspicious writable location| +25
PowerShell execution| +25
Command/script interpreter| +20
Possible command obfuscation| +25
Deleted Registry value| +5

The maximum score is limited to 100.

---

🚦 Risk Levels

Score| Risk Level
"0–29"| 🟢 LOW
"30–59"| 🟡 MEDIUM
"60–79"| 🟠 HIGH
"80–100"| 🔴 CRITICAL

---

🔄 Detection Pipeline

┌──────────────────────┐
│   Windows Registry   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Registry Snapshot  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Change Detection    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Risk Analysis      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Risk Score 0–100    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Security Alert       │
└──────────────────────┘

---

🔐 Security Use Cases

This project can help identify:

- Malware persistence
- Unauthorized startup programs
- Suspicious PowerShell persistence
- Executables launched from user-writable directories
- Script-based persistence
- Unexpected Registry modifications
- Potential endpoint compromise

---

👨‍💻 SOC Analyst Workflow

A detected Registry modification should not automatically be considered malicious.

A SOC Analyst can investigate:

Registry Alert
      ↓
Identify the modified key
      ↓
Identify the Registry value
      ↓
Analyze referenced executable/script
      ↓
Check file hash
      ↓
Check digital signature
      ↓
Identify responsible process
      ↓
Review Windows Event Logs / Sysmon
      ↓
Determine if activity is legitimate

---

⚠️ Current Limitations

The current version uses periodic Registry snapshots.

It does not yet provide:

- Process attribution
- Windows Event Log integration
- Sysmon integration
- File hash analysis
- Digital signature verification
- Automatic remediation
- SIEM integration
- Registry subkey monitoring
- Native Windows Registry change notifications

---

🗺️ Roadmap

- [x] Registry snapshot monitoring
- [x] Detect created values
- [x] Detect modified values
- [x] Detect deleted values
- [x] Risk scoring
- [x] Suspicious command detection
- [ ] JSON alert logging
- [ ] Persistent log file
- [ ] Colored terminal interface
- [ ] Process attribution
- [ ] Windows Event Log integration
- [ ] Sysmon integration
- [ ] File hash calculation
- [ ] Digital signature verification
- [ ] Configurable Registry keys
- [ ] SIEM-friendly output
- [ ] Native Registry notification API
- [ ] Production-ready alerting

---

🧪 Testing

For testing, use a dedicated Windows test environment or a Registry value that you control.

The monitor should report:

VALUE_CREATED
VALUE_MODIFIED
VALUE_DELETED

when a monitored value changes.

---

⚠️ Disclaimer

This project is intended for:

- Defensive security
- Endpoint monitoring
- Cybersecurity research
- SOC Analyst training
- Educational purposes

Only monitor systems and Registry locations that you are authorized to monitor.

---

📄 License

This project is licensed under the MIT License.

---

⭐ Project Goal

The long-term goal is to evolve this project from a simple Registry change monitor into a production-ready Windows endpoint detection component capable of generating high-quality security alerts for SOC environments.
