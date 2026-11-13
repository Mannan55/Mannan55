#!/usr/bin/env python3
"""
audit_portfolio.py
Comprehensive public repository hygiene, documentation, and security posture auditor.
Evaluates repository metadata, documentation links, CI workflows, and licensing.
Outputs a structured Markdown report to GITHUB_STEP_SUMMARY and stdout.

Strictly zero em dashes (U+2014) in all output strings and templates.
"""

import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error

USERNAME = os.environ.get("GITHUB_ACTOR", "Mannan55")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

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


def check_documentation_links(repo_name, default_branch="main"):
    """
    Checks that core documentation references in repository exist.
    Inspects README content for relative doc links.
    """
    st, readme_data = fetch_json(f"https://api.github.com/repos/{USERNAME}/{repo_name}/readme")
    if st != 200 or not readme_data or "content" not in readme_data:
        return False, ["README not found"]

    broken_links = []
    try:
        readme_text = base64.b64decode(readme_data["content"]).decode("utf-8", errors="replace")
        # Find relative markdown links e.g. [title](docs/...) or [license](LICENSE)
        relative_links = re.findall(r'\[([^\]]+)\]\(((?!https?:\/\/|mailto:|#)[^)]+)\)', readme_text)
        
        # Test up to first 5 relative links via GitHub Contents API
        for label, rel_path in relative_links[:5]:
            clean_path = rel_path.split("#")[0].strip()
            if not clean_path:
                continue
            st_link, _ = fetch_json(f"https://api.github.com/repos/{USERNAME}/{repo_name}/contents/{clean_path}")
            if st_link not in (200, 301, 302):
                broken_links.append(f"Unresolved reference: `{clean_path}`")
    except Exception as e:
        broken_links.append(f"Link check error: {e}")

    return True, broken_links


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
        recommendations.append("Add a concise description explaining the project scope.")
    elif len(desc.strip()) < 20:
        issues.append("Short description")
        recommendations.append("Expand description to highlight technical capabilities.")

    # 2. Topics check
    if not topics:
        issues.append("Missing topics")
        recommendations.append("Add relevant domain tags (for example: soc, detection-engineering, python).")

    # 3. License check
    if not has_license:
        issues.append("Missing LICENSE")
        recommendations.append("Add a standard open-source license file.")

    # 4. README & Documentation link check
    has_readme, broken_links = check_documentation_links(name, default_branch)
    if not has_readme:
        issues.append("Missing README")
        recommendations.append("Add comprehensive setup and architecture documentation.")
    elif broken_links:
        issues.append(f"Broken links ({len(broken_links)})")
        for bl in broken_links:
            recommendations.append(f"Fix link: {bl}")

    # 5. CI / Verification check
    st_wf, workflows = fetch_json(f"https://api.github.com/repos/{USERNAME}/{name}/actions/workflows")
    has_ci = (st_wf == 200 and workflows and workflows.get("total_count", 0) > 0)
    if not has_ci and not archived and not fork:
        recommendations.append("Configure automated CI workflow for testing and verification.")

    score = 100
    if not has_readme:
        score -= 35
    if broken_links:
        score -= 15
    if not desc.strip():
        score -= 20
    if not topics:
        score -= 15
    if not has_license:
        score -= 15

    score = max(0, score)

    status_badge = "Healthy" if score >= 85 else ("Needs Attention" if score >= 60 else "Action Required")

    return {
        "name": name,
        "url": html_url,
        "score": score,
        "status": status_badge,
        "has_readme": "Yes" if has_readme else "No",
        "has_license": "Yes" if has_license else "No",
        "has_ci": "Yes" if has_ci else "No",
        "topics_count": len(topics),
        "issues": issues,
        "recommendations": recommendations,
        "archived": archived,
        "fork": fork
    }


def generate_report(results):
    lines = []
    lines.append("# Public Portfolio Quality and Health Audit")
    lines.append(f"**Target Account:** [@{USERNAME}](https://github.com/{USERNAME})")
    lines.append("**Objective:** Maintain recruiter-ready presentation and documentation across public repositories.\n")

    lines.append("| Repository | Health Status | Score | README | License | CI | Topics | Primary Findings |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")

    for r in results:
        issues_str = ", ".join(r["issues"]) if r["issues"] else "Clean (healthy)"
        lines.append(f"| [{r['name']}]({r['url']}) | {r['status']} | **{r['score']}/100** | {r['has_readme']} | {r['has_license']} | {r['has_ci']} | {r['topics_count']} tags | {issues_str} |")

    lines.append("\n### Prioritized Maintenance Recommendations\n")
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
    step_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
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

    if step_summary_path:
        try:
            with open(step_summary_path, "a", encoding="utf-8") as f:
                f.write("\n" + report_md + "\n")
            print(f"[SUCCESS] Wrote audit report to {step_summary_path}")
        except Exception as e:
            print(f"[WARN] Failed writing to step summary: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
