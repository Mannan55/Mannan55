import unittest
import os
import re

WORKFLOWS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows"))

class TestWorkflowYAML(unittest.TestCase):

    def setUp(self):
        self.sync_path = os.path.join(WORKFLOWS_DIR, "profile-activity-sync.yml")
        self.audit_path = os.path.join(WORKFLOWS_DIR, "portfolio-audit.yml")

    def test_workflow_files_exist(self):
        self.assertTrue(os.path.exists(self.sync_path))
        self.assertTrue(os.path.exists(self.audit_path))

    def test_sync_workflow_configuration(self):
        with open(self.sync_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check triggers
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("cron: '0 2 * * *'", content)

        # Check concurrency
        self.assertIn("concurrency:", content)
        self.assertIn("group: profile-activity-sync", content)

        # Check permissions
        self.assertIn("permissions:", content)
        self.assertIn("contents: write", content)

        # Check action SHA pinning
        self.assertRegex(content, r'actions/checkout@[a-f0-9]{40}')
        self.assertRegex(content, r'actions/setup-python@[a-f0-9]{40}')

        # Check idempotency git diff check
        self.assertIn("git diff --quiet README.md", content)
        self.assertIn("[skip ci]", content)

    def test_audit_workflow_configuration(self):
        with open(self.audit_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check triggers
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("cron: '0 3 * * 1'", content)

        # Check permissions: read-only
        self.assertIn("permissions:", content)
        self.assertIn("contents: read", content)
        self.assertNotIn("contents: write", content)

        # Check action SHA pinning
        self.assertRegex(content, r'actions/checkout@[a-f0-9]{40}')
        self.assertRegex(content, r'actions/setup-python@[a-f0-9]{40}')

if __name__ == "__main__":
    unittest.main()
