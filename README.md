# 🌐 Network Scanner Tool

A Python-based local network scanner that discovers all connected devices, resolves hostnames, and detects open ports/services. Includes a web UI built with Flask.

---

## 🖼️ Screenshots
> *(Add screenshots after running)*

## 🚀 Live Demo
> *(Deploy on Render and add link here)*

---

## ✨ Features

- ✅ Auto-detects your local IP and subnet
- ✅ Pings all 254 hosts in the /24 range concurrently
- ✅ Reverse DNS hostname resolution
- ✅ Detects open ports: SSH, HTTP, HTTPS, RDP, SMB, Telnet
- ✅ Multi-threaded scanning (fast — ~30 seconds for full subnet)
- ✅ Web UI with live results table
- ✅ Saves scan report to `.txt` file
- ✅ Works on Windows, Linux, and macOS

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Scanning | socket, subprocess, concurrent.futures |
| Frontend | HTML, CSS, JS |
| Concepts | Networking, IP Addressing, Port Scanning |

---

## ⚙️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/KaivalyaIngole/network-scanner.git
cd network-scanner

# 2. Install dependencies
pip install flask

# 3a. Run as CLI tool
python scanner.py

# 3b. OR run with Web UI
python app.py
# Open: http://localhost:5000
```

---

## 📁 Project Structure

```
network-scanner/
├── scanner.py        ← Core scanning logic (CLI)
├── app.py            ← Flask web server
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    └── index.html    ← Web UI
```

---

## 🔐 How It Works

1. Detects your machine's local IP (e.g. `192.168.1.5`)
2. Derives subnet range (e.g. `192.168.1.0/24`)
3. Pings all 254 host IPs using **multithreading**
4. For live hosts: resolves hostname via **reverse DNS**
5. Checks 7 common ports using **socket connections**
6. Displays results in terminal or web UI

---

## ⚠️ Disclaimer

This tool is for **educational purposes and authorized network scanning only**. Only scan networks you own or have explicit permission to scan. Unauthorized scanning may be illegal.

---

## 👨‍💻 Author

**Kaivalya Ingole** — Cybersecurity Enthusiast | IT Support | Developer  
🔗 [GitHub](https://github.com/KaivalyaIngole)
