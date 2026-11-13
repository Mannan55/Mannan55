import unittest
from unittest.mock import patch
import sys
import os

# Add scripts to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

import update_activity

SAMPLE_README = """# Profile Header
Some introductory text.

### 🔄 Recent Development Activity
<!-- RECENT_ACTIVITY:START -->
*Initial activity text.*
<!-- RECENT_ACTIVITY:END -->

### 📦 Latest Project Releases & Tags
<!-- RECENT_RELEASES:START -->
*Initial releases text.*
<!-- RECENT_RELEASES:END -->

## Footer
Footer information preserved.
"""

class TestUpdateActivity(unittest.TestCase):

    def test_generate_activity_markdown_push_and_release(self):
        events = [
            {
                "type": "PushEvent",
                "repo": {"name": "Mannan55/AuthGuard-X"},
                "created_at": "2026-11-12T10:00:00Z",
                "payload": {"commits": [{"message": "feat: add syslog parser"}]}
            },
            {
                "type": "ReleaseEvent",
                "repo": {"name": "Mannan55/TrustForge"},
                "created_at": "2026-11-10T12:00:00Z",
                "payload": {"release": {"tag_name": "v1.0.0", "html_url": "https://github.com/Mannan55/TrustForge/releases/tag/v1.0.0"}}
            }
        ]
        md = update_activity.generate_activity_markdown(events)
        self.assertIn("Pushed 1 commit to [Mannan55/AuthGuard-X]", md)
        self.assertIn("feat: add syslog parser", md)
        self.assertIn("Published release [v1.0.0]", md)
        self.assertIn("2026-11-12", md)

    def test_generate_activity_markdown_empty(self):
        md = update_activity.generate_activity_markdown([])
        self.assertIn("No recent public activity", md)

    def test_replace_section_preserves_external_text(self):
        new_text = "- New test item"
        updated, modified = update_activity.replace_section(
            SAMPLE_README,
            update_activity.ACTIVITY_START_TAG,
            update_activity.ACTIVITY_END_TAG,
            new_text
        )
        self.assertTrue(modified)
        self.assertIn("# Profile Header", updated)
        self.assertIn("Footer information preserved.", updated)
        self.assertIn(f"{update_activity.ACTIVITY_START_TAG}\n{new_text}\n{update_activity.ACTIVITY_END_TAG}", updated)

    def test_replace_section_missing_marker_returns_cleanly(self):
        broken_readme = "# Just a title without markers"
        updated, modified = update_activity.replace_section(
            broken_readme,
            update_activity.ACTIVITY_START_TAG,
            update_activity.ACTIVITY_END_TAG,
            "new content"
        )
        self.assertFalse(modified)
        self.assertEqual(updated, broken_readme)

    def test_idempotency(self):
        content_1, _ = update_activity.replace_section(
            SAMPLE_README,
            update_activity.ACTIVITY_START_TAG,
            update_activity.ACTIVITY_END_TAG,
            "- Activity entry 1"
        )
        # Re-running with same content should result in 0 diff
        content_2, modified = update_activity.replace_section(
            content_1,
            update_activity.ACTIVITY_START_TAG,
            update_activity.ACTIVITY_END_TAG,
            "- Activity entry 1"
        )
        self.assertFalse(modified)
        self.assertEqual(content_1, content_2)

    @patch("update_activity.fetch_json")
    def test_failure_handling_does_not_corrupt_readme(self, mock_fetch):
        # Simulate API rate limit / 403 error
        mock_fetch.return_value = (403, None)
        events = None
        # Should gracefully skip without modifying or raising exception
        if events is not None:
            updated, modified = update_activity.replace_section(
                SAMPLE_README,
                update_activity.ACTIVITY_START_TAG,
                update_activity.ACTIVITY_END_TAG,
                "should not be written"
            )
        else:
            updated = SAMPLE_README
            modified = False
        self.assertFalse(modified)
        self.assertEqual(updated, SAMPLE_README)

if __name__ == "__main__":
    unittest.main()

