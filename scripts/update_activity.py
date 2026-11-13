#!/usr/bin/env python3
"""
update_activity.py
Synchronizes genuine public GitHub activity and releases into README.md markers.
Idempotent, fails gracefully on API errors, never alters text outside designated markers.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

USERNAME = os.environ.get("GITHUB_ACTOR", "Mannan55")
README_PATH = os.environ.get("README_PATH", "README.md")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

ACTIVITY_START_TAG = "<!-- RECENT_ACTIVITY:START -->"
ACTIVITY_END_TAG = "<!-- RECENT_ACTIVITY:END -->"
RELEASES_START_TAG = "<!-- RECENT_RELEASES:START -->"
RELEASES_END_TAG = "<!-- RECENT_RELEASES:END -->"

HEADERS = {
    "User-Agent": f"Mozilla/5.0 ProfileSync/{USERNAME}",
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
        print(f"[WARN] HTTP {e.code} fetching {url}", file=sys.stderr)
        return e.code, None
    except Exception as e:
        print(f"[WARN] Error fetching {url}: {e}", file=sys.stderr)
        return 0, None


def format_timestamp(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return iso_str[:10] if iso_str else "N/A"


def generate_activity_markdown(events):
    if not events:
        return "*No recent public activity recorded in the last 30 days.*"

    items = []
    seen = set()
    for ev in events:
        ev_type = ev.get("type")
        repo_name = ev.get("repo", {}).get("name", "")
        repo_url = f"https://github.com/{repo_name}"
        created_at = format_timestamp(ev.get("created_at", ""))

        desc = None
        if ev_type == "PushEvent":
            payload = ev.get("payload", {})
            commits = payload.get("commits", [])
            count = payload.get("size", len(commits))
            ref = payload.get("ref", "").replace("refs/heads/", "")
            
            if commits:
                msg = commits[0].get("message", "").split("\n")[0]
                if len(msg) > 60:
                    msg = msg[:57] + "..."
                commit_desc = f" (`{msg}`)"
            elif ref:
                commit_desc = f" to `{ref}`"
            else:
                commit_desc = ""

            count_str = f"{count} commit{'s' if count != 1 else ''}" if count > 0 else "updates"
            desc = f"Pushed {count_str} to [{repo_name}]({repo_url}){commit_desc}"
        elif ev_type == "ReleaseEvent":
            rel_name = ev.get("payload", {}).get("release", {}).get("tag_name", "release")
            rel_url = ev.get("payload", {}).get("release", {}).get("html_url", repo_url)
            desc = f"Published release [{rel_name}]({rel_url}) in [{repo_name}]({repo_url})"
        elif ev_type == "CreateEvent":
            ref_type = ev.get("payload", {}).get("ref_type", "branch")
            ref = ev.get("payload", {}).get("ref", "")
            if ref_type == "repository":
                desc = f"Created repository [{repo_name}]({repo_url})"
            elif ref:
                desc = f"Created {ref_type} `{ref}` in [{repo_name}]({repo_url})"
        elif ev_type == "PullRequestEvent":
            action = ev.get("payload", {}).get("action", "opened")
            pr = ev.get("payload", {}).get("pull_request", {})
            pr_title = pr.get("title", "")
            pr_url = pr.get("html_url", repo_url)
            desc = f"{action.capitalize()} PR [#{pr.get('number', '')} {pr_title}]({pr_url}) in [{repo_name}]({repo_url})"
        elif ev_type == "IssuesEvent":
            action = ev.get("payload", {}).get("action", "opened")
            issue = ev.get("payload", {}).get("issue", {})
            issue_title = issue.get("title", "")
            issue_url = issue.get("html_url", repo_url)
            desc = f"{action.capitalize()} issue [#{issue.get('number', '')} {issue_title}]({issue_url}) in [{repo_name}]({repo_url})"

        if desc and desc not in seen:
            seen.add(desc)
            items.append(f"- 🕒 **{created_at}** — {desc}")

        if len(items) >= 6:
            break

    if not items:
        return "*No recent public event highlights recorded.*"

    return "\n".join(items)


def generate_releases_markdown(repos):
    if not repos:
        return "*No published releases currently listed.*"

    items = []
    for r in repos:
        repo_name = r.get("name")
        if not repo_name:
            continue
        st, releases = fetch_json(f"https://api.github.com/repos/{USERNAME}/{repo_name}/releases")
        if st == 200 and releases:
            latest = releases[0]
            tag = latest.get("tag_name", "v1.0.0")
            url = latest.get("html_url", f"https://github.com/{USERNAME}/{repo_name}")
            date = format_timestamp(latest.get("published_at", ""))
            name = latest.get("name") or tag
            items.append(f"- 🏷️ **[{repo_name}]({url})** — [{name}]({url}) ({date})")

    if not items:
        return "*Active repositories use source tags and trunk-based CI verification (`main`). Official tagged release distribution packages will appear here.*"

    return "\n".join(items)


def replace_section(content, start_tag, end_tag, new_text):
    pattern = rf"({re.escape(start_tag)}\n).*?(\n{re.escape(end_tag)})"
    if not re.search(pattern, content, flags=re.DOTALL):
        print(f"[ERROR] Markers {start_tag} ... {end_tag} not found in README!", file=sys.stderr)
        return content, False
    replacement = rf"\g<1>{new_text}\g<2>"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return updated_content, (updated_content != content)


def main():
    if not os.path.exists(README_PATH):
        print(f"[ERROR] Target README not found at {README_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(README_PATH, "r", encoding="utf-8") as f:
        original_content = f.read()

    print(f"[INFO] Fetching public events for user '{USERNAME}'...")
    st_events, events = fetch_json(f"https://api.github.com/users/{USERNAME}/events/public?per_page=30")

    print(f"[INFO] Fetching public repositories for user '{USERNAME}'...")
    st_repos, repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=50")

    content = original_content

    # Update activity section if events request succeeded
    if st_events == 200 and events is not None:
        activity_md = generate_activity_markdown(events)
        content, _ = replace_section(content, ACTIVITY_START_TAG, ACTIVITY_END_TAG, activity_md)
    else:
        print("[WARN] Skipping activity update due to API unavailability/rate limit.")

    # Update releases section if repos request succeeded
    if st_repos == 200 and repos is not None:
        releases_md = generate_releases_markdown(repos)
        content, _ = replace_section(content, RELEASES_START_TAG, RELEASES_END_TAG, releases_md)
    else:
        print("[WARN] Skipping releases update due to API unavailability/rate limit.")

    if content != original_content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] README.md updated with latest activity and releases.")
    else:
        print("[INFO] Content identical. No changes written (idempotent).")


if __name__ == "__main__":
    main()
