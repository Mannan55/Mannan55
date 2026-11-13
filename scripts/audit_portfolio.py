#!/usr/bin/env python3
"""
audit_portfolio.py
Lightweight portfolio quality audit for Mannan55's public repositories.
Evaluates repository hygiene, metadata completeness, topics, and documentation.
Outputs a structured Markdown report to GITHUB_STEP_SUMMARY and stdout.
"""

import os
import sys
import json
import urllib.request
import urllib.error

USERNAME = os.environ.get("GITHUB_ACTOR", "Mannan55")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
STEP_SUMMARY_PATH = os.environ.get("GITHUB_STEP_SUMMARY")

HEADERS = {
    "User-Agent": f"Mozilla/5.0 PortfolioAudit/{USERNAME}",
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, None


def audit_repository(repo):
    name = repo.get("name")
    html_url = repo.get("html_url")
    desc = repo.get("description") or ""
    topics = repo.get("topics") or []
    has_license = bool(repo.get("license"))
    default_branch = repo.get("default_branch", "main")
    archived = repo.get("archived", False)
    fork = repo.get("fork", False)

    issues = []
    recommendations = []

    # 1. Description check
    if not desc.strip():
        issues.append("Missing description")
        recommendations.append("Add a concise 1-sentence description highlighting the project's purpose.")
    elif len(desc.strip()) < 20:
        issues.append("Short description")
        recommendations.append("Expand description to explain technical scope and domain.")

    # 2. Topics check
    if not topics:
        issues.append("Missing topics")
        recommendations.append("Add 4–6 relevant tags (e.g. `soc`, `incident-response`, `mitre-attack`, `python`).")

    # 3. License check
    if not has_license:
        issues.append("Missing LICENSE")
        recommendations.append("Add standard open-source license (e.g. MIT).")

    # 4. README check via API
    st_rm, _ = fetch_json(f"https://api.github.com/repos/{USERNAME}/{name}/readme")
    has_readme = (st_rm == 200)
    if not has_readme:
        issues.append("Missing README")
        recommendations.append("Create a comprehensive README detailing architecture and setup.")

    score = 100
    if not has_readme:
        score -= 40
    if not desc.strip():
        score -= 25
    if not topics:
        score -= 20
    if not has_license:
        score -= 15

    score = max(0, score)

    status_badge = "🟢 Excellent" if score >= 85 else ("🟡 Needs Attention" if score >= 60 else "🔴 Action Required")

    return {
        "name": name,
        "url": html_url,
        "score": score,
        "status": status_badge,
        "has_readme": "✅ Yes" if has_readme else "❌ No",
        "has_license": "✅ Yes" if has_license else "❌ No",
        "topics_count": len(topics),
        "issues": issues,
        "recommendations": recommendations,
        "archived": archived,
        "fork": fork
    }


def generate_report(results):
    lines = []
    lines.append("# 🛡️ Automated Public Portfolio Quality Audit")
    lines.append(f"**Target Account:** [@{USERNAME}](https://github.com/{USERNAME})  ")
    lines.append("**Objective:** Maintain recruiter-ready presentation across all public repositories.\n")

    lines.append("| Repository | Health Status | Score | README | License | Topics | Primary Findings |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :--- |")

    for r in results:
        issues_str = ", ".join(r["issues"]) if r["issues"] else "None (healthy)"
        lines.append(f"| [{r['name']}]({r['url']}) | {r['status']} | **{r['score']}/100** | {r['has_readme']} | {r['has_license']} | {r['topics_count']} tags | {issues_str} |")

    lines.append("\n### 📋 Prioritized Recommendations\n")
    has_recs = False
    for r in results:
        if r["recommendations"]:
            has_recs = True
            lines.append(f"#### [{r['name']}]({r['url']})")
            for rec in r["recommendations"]:
                lines.append(f"- {rec}")

    if not has_recs:
        lines.append("*All public repositories meet quality, documentation, and metadata standards.*")

    lines.append("\n---\n*Report generated automatically by `scripts/audit_portfolio.py`.*")
    return "\n".join(lines)


def main():
    print(f"[INFO] Auditing public repositories for user '{USERNAME}'...")
    st, repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated")
    if st != 200 or not repos:
        print(f"[ERROR] Failed to fetch repositories (HTTP {st})", file=sys.stderr)
        sys.exit(1)

    results = []
    for r in repos:
        results.append(audit_repository(r))

    report_md = generate_report(results)
    print("\n" + report_md + "\n")

    if STEP_SUMMARY_PATH:
        try:
            with open(STEP_SUMMARY_PATH, "a", encoding="utf-8") as f:
                f.write("\n" + report_md + "\n")
            print(f"[SUCCESS] Wrote audit report to {STEP_SUMMARY_PATH}")
        except Exception as e:
            print(f"[WARN] Failed writing to step summary: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
