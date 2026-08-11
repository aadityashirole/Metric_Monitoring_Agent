# Automated Metric Monitoring Agent

An end-to-end Python data pipeline that ingests time-series metrics from Excel, validates schema integrity, detects statistical anomalies using Z-scores, executes dimensional root-cause analysis, and triggers automated email alerts via SMTP.

## Core Features
* **Data Ingestion & Validation:** Enforces strict datetime and numerical type checking on raw Excel inputs.
* **Statistical Anomaly Detection:** Applies Z-score normalization ($Z = \frac{X - \mu}{\sigma}$) to flag deviations beyond configurable thresholds.
* **Dimensional Root-Cause Analysis:** Quantifies baseline drops to isolate specific contributing segments (e.g., regional revenue drops).
* **Zero-Noise Alerting:** Incorporates a guard clause to trigger email notifications only when actionable anomalies occur.

## Project Structure
* `ingest.py` - Data loading and schema validation
* `anomaly_engine.py` - Statistical anomaly calculation logic
* `root_cause.py` - Dimensional drop & impact breakdown engine
* `alert_engine.py` - Pipeline controller & SMTP notification dispatch
* `create_excel.py` - Data generator for local testing

## Tech Stack
* **Language:** Python 3.10+
* **Libraries:** Pandas, NumPy, OpenPyXL
* **Protocol:** SMTP (`smtplib`, `email.mime`)