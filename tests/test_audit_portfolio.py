import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

import audit_portfolio

class TestAuditPortfolio(unittest.TestCase):

    @patch("audit_portfolio.fetch_json")
    def test_audit_repository_healthy(self, mock_fetch):
        # Mock README check returning 200
        mock_fetch.return_value = (200, {"content": "dGVzdA=="})
        repo = {
            "name": "AuthGuard-X",
            "html_url": "https://github.com/Mannan55/AuthGuard-X",
            "description": "Comprehensive local SOC training platform with incident response.",
            "topics": ["soc", "detection-engineering", "python"],
            "license": {"key": "mit"},
            "default_branch": "main",
            "archived": False,
            "fork": False
        }
        res = audit_portfolio.audit_repository(repo)
        self.assertEqual(res["score"], 100)
        self.assertIn("Excellent", res["status"])
        self.assertEqual(len(res["issues"]), 0)

    @patch("audit_portfolio.fetch_json")
    def test_audit_repository_missing_metadata(self, mock_fetch):
        # Mock README check returning 404
        mock_fetch.return_value = (404, None)
        repo = {
            "name": "empty-project",
            "html_url": "https://github.com/Mannan55/empty-project",
            "description": "",
            "topics": [],
            "license": None,
            "default_branch": "main",
            "archived": False,
            "fork": False
        }
        res = audit_portfolio.audit_repository(repo)
        self.assertEqual(res["score"], 0)
        self.assertIn("Action Required", res["status"])
        self.assertIn("Missing description", res["issues"])
        self.assertIn("Missing topics", res["issues"])
        self.assertIn("Missing LICENSE", res["issues"])
        self.assertIn("Missing README", res["issues"])

    def test_generate_report_markdown(self):
        results = [
            {
                "name": "AuthGuard-X",
                "url": "https://github.com/Mannan55/AuthGuard-X",
                "score": 80,
                "status": "🟢 Excellent",
                "has_readme": "✅ Yes",
                "has_license": "✅ Yes",
                "topics_count": 0,
                "issues": ["Missing topics"],
                "recommendations": ["Add 4-6 relevant tags"],
                "archived": False,
                "fork": False
            }
        ]
        md = audit_portfolio.generate_report(results)
        self.assertIn("# 🛡️ Automated Public Portfolio Quality Audit", md)
        self.assertIn("AuthGuard-X", md)
        self.assertIn("Missing topics", md)
        self.assertIn("Add 4-6 relevant tags", md)

if __name__ == "__main__":
    unittest.main()
