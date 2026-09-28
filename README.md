# CyberScope

CyberScope is a Flask-based network security scanner for **authorized local/private targets**. It provides the same core workflow as the reference project while using a completely different dashboard/UI design.

## Included features

- TCP Scan
- UDP Scan
- SYN Scan
- Service Version Detection
- OS Detection
- Aggressive Scan
- HTML report generation
- PDF report download
- XML report download
- Email PDF report
- Scan history
- Host, OS, port and service details
- Defensive recommendations

## Run

1. Install Nmap and make sure it is available on PATH.
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000`.

Only scan systems you own or have explicit permission to test.
