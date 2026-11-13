# Mannan Shah

<p align="left">
  <strong>Aspiring SOC Analyst & Cybersecurity Engineer</strong> • B.Sc. IT (Expected 2027)<br>
  <em>Focus: Incident Investigation, Detection Engineering, Security Telemetry, and AI-Assisted Compliance</em>
</p>

<p align="left">
  <a href="https://www.linkedin.com/in/mannan-shah"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn Profile" /></a>
  <a href="https://github.com/Mannan55"><img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub Profile" /></a>
  <img src="https://img.shields.io/badge/Location-Mumbai%2C%20India-blue" alt="Location: Mumbai, India" />
  <img src="https://img.shields.io/badge/Status-Actively%20Building%20%26%20Learning-success" alt="Status" />
</p>

---

## 🛡️ Profile Overview

Third-year **B.Sc. Information Technology** student at Usha Pravin Gandhi College, Mumbai (graduating in 2027), targeting entry-level **Security Operations Center (SOC) Analyst**, **Cybersecurity Internship**, and **Junior Security Engineering** positions.

My technical work emphasizes **evidence-grounded engineering**: building local-first simulation and investigation environments, parsing heterogenous security telemetry, designing detection rules mapped to **MITRE ATT&CK**, and automating regulatory compliance verification.

---

## 🔬 Featured Engineering Projects

### 1. [AuthGuard-X](https://github.com/Mannan55/AuthGuard-X) — Local-First SOC Training & Investigation Platform

> A self-contained, local-first practice control room for security operations, detection testing, and incident investigation.

[![CI Verification](https://github.com/Mannan55/AuthGuard-X/actions/workflows/ci.yml/badge.svg)](https://github.com/Mannan55/AuthGuard-X/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Mannan55/AuthGuard-X/blob/main/LICENSE)

* **Telemetry Ingestion:** Parses RFC 5424 syslog, Linux authentication logs, Windows failed-login records, Palo Alto firewall traffic logs, and NDJSON streams into structured SQLite storage.
* **Detection Engineering:** Rule-based detection engine featuring configurable time-window correlation and contextual **MITRE ATT&CK** technique classification.
* **Investigation Workflow:** Full incident response lifecycle management (**New → Investigating → Contained → Resolved**), evidence tracking, and analyst case notes.
* **Reporting & Integrity:** Deterministic findings verification with structured HTML and JSON export for incident review.
* **Security Controls:** Session authentication, bcrypt password hashing, CSRF defense, rate limiting, and role-based access checks.
* **Scope Boundary:** *Engineered as a local-first training simulator and investigation workspace. Generates synthetic training records; does not interact with remote enterprise endpoints.*

**Stack:** Python 3.11+, Flask, SQLite, Vanilla JavaScript, Chart.js, Pytest, GitHub Actions CI.

---

### 2. [TrustForge](https://github.com/Mannan55/TrustForge) — DPDP Compliance & Privacy Assessment Platform

> An automated compliance auditing, risk assessment, and decision-support platform benchmarked against India's Digital Personal Data Protection (DPDP) Act 2023.

[![CI Verification](https://github.com/Mannan55/TrustForge/actions/workflows/ci.yml/badge.svg)](https://github.com/Mannan55/TrustForge/actions/workflows/ci.yml)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)

* **Hybrid Retrieval Architecture:** Integrates dense vector search with sparse BM25 retrieval fused via Reciprocal Rank Fusion ($k=60$) for precise statutory grounding.
* **Deterministic Trust Engine:** Evaluates compliance across six statutory pillars (Privacy, Security, Transparency, Governance, Lifecycle, Rights) with mandatory gating controls.
* **Multi-Criteria Model Selection:** Implements TOPSIS decision criteria to benchmark 10 model configurations under a strict zero-commercial-spend operational boundary.
* **Durable Security Store:** Local-first storage engine with tenant-isolated directories, SHA-256 evidence hashing, and an append-only audit trail.
* **Scope Boundary:** *Developed as an evidence-grounded research prototype and decision-support system. Does not constitute formal legal counsel or statutory regulatory certification.*

**Stack:** React 18, Vite, TypeScript, Tailwind CSS, Node.js Express, Python 3.12, SQLite, PyTest, Playwright.

---

## 🛠️ Technical Competencies

| Domain | Tools & Technologies |
| :--- | :--- |
| **Security Operations & Detection** | MITRE ATT&CK Mapping, Alert Triage, Time-Window Event Correlation, Synthetic Attack Simulation, Incident Case Lifecycle Management |
| **Log Analysis & Telemetry** | Syslog (RFC 5424), Linux Auth Logs, Windows Event Logs, Palo Alto Firewall Logs, NDJSON Ingestion, Wireshark |
| **Networking & Systems** | TCP/IP Suite, Subnetting, VLANs, Routing/Switching Fundamentals, Linux Administration, Windows Administration |
| **Development & Automation** | Python, TypeScript, Node.js, Express, Flask, SQL (SQLite / PostgreSQL), HTML/CSS, Bash Scripting |
| **Testing & CI/CD** | Pytest, Playwright, GitHub Actions Workflows, Automated Code Quality & Linting |
| **Governance & Frameworks** | Digital Personal Data Protection (DPDP) Act 2023 Assessment, Evidence-Linked Auditing, Risk Scoring |

---

## 🎓 Education & Verified Credentials

* **B.Sc. in Information Technology** — Usha Pravin Gandhi College, Mumbai *(Expected Graduation: 2027)*
* **Cisco Certified Network Associate (CCNA) Coursework** — *Completed CCNA curriculum training covering IP connectivity, network access, IP services, and security fundamentals. (Training completion; not Cisco certified).*
* **Active Learning Track** — *Hands-on SOC investigation workflows, detection engineering with MITRE ATT&CK, and Certified Ethical Hacker (CEH) study curriculum (actively studying; not certified).*

---

## 📈 Engineering Telemetry & Activity

<div align="center">
  <img src="assets/profile-metrics.svg" alt="Mannan Shah Engineering Metrics" width="100%" />
</div>

<br>

### 🔄 Recent Development Activity
<!-- RECENT_ACTIVITY:START -->
*No recent public activity recorded within GitHub's 90-day event window.*
<!-- RECENT_ACTIVITY:END -->

### 📦 Latest Project Releases & Tags
<!-- RECENT_RELEASES:START -->
**Active Git Source Tags (CI Verified):**
- 🏷️ **[AuthGuard-X](https://github.com/Mannan55/AuthGuard-X/tree/v3)** — Source Tag [`v3`](https://github.com/Mannan55/AuthGuard-X/tree/v3) *(Trunk CI Verified)*
- 🏷️ **[tiny-tyrants](https://github.com/Mannan55/tiny-tyrants/tree/v1.1.0)** — Source Tag [`v1.1.0`](https://github.com/Mannan55/tiny-tyrants/tree/v1.1.0) *(Trunk CI Verified)*
- 🏷️ **[TrustForge](https://github.com/Mannan55/TrustForge/tree/v1.0.0-release)** — Source Tag [`v1.0.0-release`](https://github.com/Mannan55/TrustForge/tree/v1.0.0-release) *(Trunk CI Verified)*
<!-- RECENT_RELEASES:END -->

---

## 📬 Connect & Verification

* **LinkedIn:** [linkedin.com/in/mannan-shah](https://www.linkedin.com/in/mannan-shah)
* **GitHub Repositories:** [github.com/Mannan55](https://github.com/Mannan55)
* **Collaboration Focus:** Open to cybersecurity internships, SOC analyst training roles, and open-source detection engineering collaboration.
