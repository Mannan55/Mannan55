# Repository Metadata Optimization Proposals

**Purpose:** Provide recruiter-optimized repository descriptions and relevant GitHub topics for primary portfolio projects (**AuthGuard-X** and **TrustForge**) to maximize technical discoverability without modifying any source code.

---

## 1. AuthGuard-X

* **Current Description:** `Backend for AuthGuard-X SOC project`
* **Current Topics:** *None (`[]`)*
* **Issues:** Too brief, mentions only "Backend", does not convey that it is a full local-first SOC training and incident investigation control room.

### Proposed Metadata
* **Proposed Description:**
  > Local-first SOC training and incident investigation platform with synthetic attack simulation, multi-source log ingestion, MITRE ATT&CK detection rules, and structured case reporting.

* **Proposed Topics:**
  - `soc`
  - `security-operations`
  - `incident-response`
  - `detection-engineering`
  - `mitre-attack`
  - `log-analysis`
  - `python`
  - `flask`
  - `cybersecurity`

### How to Apply
```bash
# Using GitHub CLI (when authenticated):
gh repo edit Mannan55/AuthGuard-X \
  --description "Local-first SOC training and incident investigation platform with synthetic attack simulation, multi-source log ingestion, MITRE ATT&CK detection rules, and structured case reporting." \
  --add-topic soc,security-operations,incident-response,detection-engineering,mitre-attack,log-analysis,python,flask,cybersecurity
```
*Or via the GitHub web interface: Go to https://github.com/Mannan55/AuthGuard-X, click the ⚙️ icon next to "About" on the right sidebar, and update the description and topics.*

---

## 2. TrustForge

* **Current Description:**
  > TrustForge is an AI-powered Digital Trust Platform that helps organizations assess, improve, and demonstrate compliance with the Digital Personal Data Protection (DPDP) Act through intelligent assessments, website analysis, document evaluation, and evidence-based trust scoring.
* **Current Topics:** *None (`[]`)*
* **Assessment:** The current description is descriptive, but topics are empty, reducing visibility for data privacy, RAG, and compliance engineering searches.

### Proposed Metadata
* **Refined Description:**
  > AI-assisted DPDP Act 2023 compliance auditing and privacy risk assessment platform featuring hybrid RAG, deterministic trust scoring, and TOPSIS model benchmarking.

* **Proposed Topics:**
  - `dpdp-act-2023`
  - `data-privacy`
  - `compliance-automation`
  - `rag`
  - `risk-assessment`
  - `typescript`
  - `react`
  - `python`
  - `security-audit`

### How to Apply
```bash
# Using GitHub CLI (when authenticated):
gh repo edit Mannan55/TrustForge \
  --description "AI-assisted DPDP Act 2023 compliance auditing and privacy risk assessment platform featuring hybrid RAG, deterministic trust scoring, and TOPSIS model benchmarking." \
  --add-topic dpdp-act-2023,data-privacy,compliance-automation,rag,risk-assessment,typescript,react,python,security-audit
```
*Or via the GitHub web interface: Go to https://github.com/Mannan55/TrustForge, click the ⚙️ icon next to "About" on the right sidebar, and update the description and topics.*

