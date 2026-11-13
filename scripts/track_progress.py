#!/usr/bin/env python3
"""
track_progress.py
Lightweight GitHub contribution and achievement progress tracker for Mannan55.
Read-only monitoring tool. Computes weekly activity consistency, pull request progress,
star counts, and achievement milestones.

Strictly zero em dashes (U+2014).
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

USERNAME = os.environ.get("GITHUB_ACTOR", "Mannan55")


def run_graphql(query):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode == 0:
        try:
            return json.loads(p.stdout)
        except Exception:
            return None
    return None


def run_gh_api(endpoint):
    cmd = ["gh", "api", endpoint]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode == 0:
        try:
            return json.loads(p.stdout)
        except Exception:
            return None
    return None


def calculate_metrics():
    query = f"""
    query {{
      user(login: "{USERNAME}") {{
        createdAt
        contributionsCollection {{
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
          restrictedContributionsCount
          contributionCalendar {{
            totalContributions
            weeks {{
              contributionDays {{
                contributionCount
                date
                weekday
              }}
            }}
          }}
        }}
        repositories(first: 50, privacy: PUBLIC, isFork: false) {{
          totalCount
          nodes {{
            name
            stargazerCount
            forkCount
            openIssues: issues(states: OPEN) {{
              totalCount
            }}
          }}
        }}
      }}
    }}
    """
    data = run_graphql(query)
    if not data or "data" not in data or not data["data"].get("user"):
        print("[ERROR] Failed to query GitHub GraphQL API. Verify gh auth status.", file=sys.stderr)
        return None

    user = data["data"]["user"]
    cc = user.get("contributionsCollection", {})
    cal = cc.get("contributionCalendar", {})

    # Calculate active days in the last 30 days
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    recent_active_days = 0
    total_recent_contributions = 0
    days_by_week = [0] * 5

    weeks = cal.get("weeks", [])
    for w_idx, week in enumerate(weeks[-5:]):
        for day in week.get("contributionDays", []):
            d_str = day.get("date")
            cnt = day.get("contributionCount", 0)
            if d_str:
                d_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
                if d_obj >= thirty_days_ago:
                    if cnt > 0:
                        recent_active_days += 1
                        total_recent_contributions += cnt
                        days_by_week[w_idx] += 1

    # PR Count
    pr_count = cc.get("totalPullRequestContributions", 0)

    # Stars
    repos = user.get("repositories", {}).get("nodes", [])
    total_stars = sum(r.get("stargazerCount", 0) for r in repos)

    return {
        "total_contributions": cal.get("totalContributions", 0),
        "total_commits": cc.get("totalCommitContributions", 0),
        "total_prs": pr_count,
        "total_issues": cc.get("totalIssueContributions", 0),
        "total_reviews": cc.get("totalPullRequestReviewContributions", 0),
        "private_contributions": cc.get("restrictedContributionsCount", 0),
        "recent_30d_active_days": recent_active_days,
        "recent_30d_contributions": total_recent_contributions,
        "weekly_active_days": days_by_week,
        "total_stars": total_stars,
        "repos": repos
    }


def format_progress_report(metrics):
    if not metrics:
        return "# Progress Tracking Error\nCould not fetch metrics from GitHub."

    lines = []
    lines.append("# GitHub Contribution and Achievement Progress Dashboard")
    lines.append(f"**Target Account:** [@{USERNAME}](https://github.com/{USERNAME})")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    lines.append("## 1. Contribution Consistency Overview")
    lines.append(f"- **Total Lifetime Contributions:** {metrics['total_contributions']}")
    lines.append(f"- **Active Days (Past 30 Days):** {metrics['recent_30d_active_days']} days (Target: 16-20 days)")
    lines.append(f"- **Contributions (Past 30 Days):** {metrics['recent_30d_contributions']}")
    lines.append(f"- **Private Contributions Tracked:** {metrics['private_contributions']}")
    lines.append(f"- **Active Repositories (Public):** {len(metrics['repos'])}\n")

    lines.append("## 2. Achievement Milestones Progress")
    
    # Pull Shark progress (Base: 2 PRs, Silver: 16 PRs)
    prs = metrics["total_prs"]
    pr_target = 16
    pr_pct = min(100, int((prs / pr_target) * 100))
    lines.append(f"### Pull Shark (Current: Base Tier | Next: Silver)")
    lines.append(f"- Progress: {prs}/{pr_target} Merged PRs ({pr_pct}%)")
    lines.append(f"- Status: Active (Need {max(0, pr_target - prs)} more merged PRs for Silver tier)\n")

    # Starstruck progress (16 stars)
    stars = metrics["total_stars"]
    star_target = 16
    star_pct = min(100, int((stars / star_target) * 100))
    lines.append(f"### Starstruck (Target: Bronze Tier at 16 Stars)")
    lines.append(f"- Progress: {stars}/{star_target} Stars ({star_pct}%)")
    lines.append(f"- Status: In Progress (Need {max(0, star_target - stars)} more stars across public repositories)\n")

    # Pair Extraordinaire
    lines.append("### Pair Extraordinaire (Target: 1 Co-authored Merged PR)")
    lines.append("- Status: Pending")
    lines.append("- Requirement: Author or co-author a commit with a peer using Git co-author trailer.\n")

    # Galaxy Brain
    lines.append("### Galaxy Brain (Target: 2 Accepted Answers in Discussions)")
    lines.append("- Status: Pending")
    lines.append("- Requirement: Provide accepted technical answers in public GitHub Discussions.\n")

    lines.append("## 3. Public Repositories Health")
    lines.append("| Repository | Stars | Forks | Open Issues |")
    lines.append("| :--- | :---: | :---: | :---: |")
    for r in metrics["repos"]:
        lines.append(f"| [{r['name']}](https://github.com/{USERNAME}/{r['name']}) | {r['stargazerCount']} | {r['forkCount']} | {r['openIssues']['totalCount']} |")

    lines.append("\n---\n*Report generated locally by `scripts/track_progress.py`. Zero remote changes made.*")
    return "\n".join(lines)


def main():
    print(f"[INFO] Computing progress metrics for '{USERNAME}'...")
    metrics = calculate_metrics()
    report = format_progress_report(metrics)
    print("\n" + report + "\n")

    output_path = "docs/PROGRESS_REPORT.md"
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[SUCCESS] Saved progress report to {output_path}")
    except Exception as e:
        print(f"[WARN] Could not write report file: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

