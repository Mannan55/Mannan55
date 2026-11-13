import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

import update_activity
import audit_portfolio

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.readme_path = os.path.join(self.test_dir.name, "README.md")
        self.assets_dir = os.path.join(self.test_dir.name, "assets")
        os.makedirs(self.assets_dir, exist_ok=True)

        self.initial_readme = """# Test Profile
<!-- RECENT_ACTIVITY:START -->
*Old activity*
<!-- RECENT_ACTIVITY:END -->

<!-- RECENT_RELEASES:START -->
*Old releases*
<!-- RECENT_RELEASES:END -->
"""
        with open(self.readme_path, "w", encoding="utf-8") as f:
            f.write(self.initial_readme)

    def tearDown(self):
        self.test_dir.cleanup()

    @patch("update_activity.fetch_json")
    def test_pagination_fetches_multiple_pages(self, mock_fetch):
        page_1 = [{"id": f"ev_{i}", "type": "PushEvent", "created_at": "2026-11-12T10:00:00Z", "repo": {"name": "Mannan55/AuthGuard-X"}, "payload": {"size": 1}} for i in range(30)]
        page_2 = [{"id": f"ev_{i}", "type": "PushEvent", "created_at": "2026-11-11T10:00:00Z", "repo": {"name": "Mannan55/TrustForge"}, "payload": {"size": 2}} for i in range(30, 35)]
        
        mock_fetch.side_effect = [
            (200, page_1, "4999"),
            (200, page_2, "4998")
        ]
        
        events = update_activity.fetch_paginated_events("Mannan55", max_pages=2)
        self.assertEqual(len(events), 35)

    @patch("update_activity.fetch_json")
    def test_rate_limit_backoff_and_safety(self, mock_fetch):
        # Return 403 Rate Limit on events fetch
        mock_fetch.return_value = (403, None, "0")
        
        with patch.dict(os.environ, {"README_PATH": self.readme_path, "ASSETS_DIR": self.assets_dir}):
            update_activity.main()

        # Confirm README was NOT wiped or corrupted
        with open(self.readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, self.initial_readme)

    def test_svg_generation_valid_xml_and_theming(self):
        svg_path = os.path.join(self.assets_dir, "test-metrics.svg")
        repos = [
            {"name": "AuthGuard-X", "language": "Python", "fork": False},
            {"name": "TrustForge", "language": "TypeScript", "fork": False},
            {"name": "tiny-tyrants", "language": "JavaScript", "fork": False}
        ]
        success = update_activity.generate_metrics_svg(repos, svg_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(svg_path))

        with open(svg_path, "r", encoding="utf-8") as f:
            svg_text = f.read()

        # Validate that it's valid XML
        root = ET.fromstring(svg_text)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["width"], "820")
        self.assertEqual(root.attrib["height"], "150")

        # Validate dark mode media query
        self.assertIn("@media (prefers-color-scheme: dark)", svg_text)
        self.assertIn("Python, TypeScript, JavaScript", svg_text)

    def test_event_deduplication(self):
        # 3 identical push events to same repo on same date
        events = [
            {
                "id": "1",
                "type": "PushEvent",
                "repo": {"name": "Mannan55/AuthGuard-X"},
                "created_at": "2026-11-12T10:00:00Z",
                "payload": {"size": 1, "commits": [{"message": "fix: bug"}]}
            },
            {
                "id": "2",
                "type": "PushEvent",
                "repo": {"name": "Mannan55/AuthGuard-X"},
                "created_at": "2026-11-12T10:05:00Z",
                "payload": {"size": 1, "commits": [{"message": "fix: bug"}]}
            }
        ]
        md = update_activity.generate_activity_markdown(events)
        # Should be deduplicated to exactly 1 bullet item
        lines = [l for l in md.strip().split("\n") if l.startswith("- ")]
        self.assertEqual(len(lines), 1)

    @patch("audit_portfolio.fetch_json")
    def test_audit_workflow_end_to_end_step_summary(self, mock_fetch):
        summary_file = os.path.join(self.test_dir.name, "step_summary.md")
        mock_fetch.side_effect = [
            # 1. Repos list
            (200, [
                {"name": "AuthGuard-X", "html_url": "https://github.com/Mannan55/AuthGuard-X", "description": "Local SOC training control room", "topics": ["soc"], "license": {"key": "mit"}, "default_branch": "main", "archived": False, "fork": False}
            ]),
            # 2. README check
            (200, {"content": "dGVzdA=="}),
            # 3. Workflows check
            (200, {"total_count": 1, "workflows": [{"name": "CI"}]})
        ]

        with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary_file}):
            audit_portfolio.main()

        self.assertTrue(os.path.exists(summary_file))
        with open(summary_file, "r", encoding="utf-8") as f:
            summary = f.read()
        self.assertIn("# Public Portfolio Quality and Health Audit", summary)
        self.assertIn("AuthGuard-X", summary)

if __name__ == "__main__":
    unittest.main()
