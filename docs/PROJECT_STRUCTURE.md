# CyberScope Project Structure

- `app.py` — Flask web application and routes
- `scanner/` — Nmap scanning and target validation
- `templates/` — dashboard, results, and history pages
- `static/` — UI styles
- `database.py` — scan-history storage
- `pdf_report.py` — PDF report generation
- `xml_report.py` — XML report generation
- `email_report.py` — email delivery helper
- `recommendations.py` — defensive recommendations
- `reports/` — generated reports (ignored by Git except `.gitkeep`)
- `scanner_test.py` — lightweight unit tests that do not launch a network scan
