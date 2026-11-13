import unittest
import os
import re

README_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))

class TestReadmeIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(README_PATH, "r", encoding="utf-8") as f:
            cls.content = f.read()

    def test_readme_exists_and_non_empty(self):
        self.assertTrue(os.path.exists(README_PATH))
        self.assertGreater(len(self.content), 500)

    def test_no_personal_email_exposure(self):
        # Ensure raw personal email is not exposed in public profile README
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        matches = re.findall(email_pattern, self.content)
        # Verify no real personal email addresses are leaked
        for email in matches:
            self.fail(f"Personal email address detected in README: {email}")

    def test_required_sections_present(self):
        required_headers = [
            "Mannan Shah",
            "Featured Engineering Projects",
            "AuthGuard-X",
            "TrustForge",
            "Technical Competencies",
            "Education and Verified Credentials",
            "Engineering Telemetry and Activity",
            "Professional Verification and Contact"
        ]
        for header in required_headers:
            self.assertIn(header, self.content, f"Missing required header/section: '{header}'")

    def test_comment_markers_intact(self):
        markers = [
            "<!-- RECENT_ACTIVITY:START -->",
            "<!-- RECENT_ACTIVITY:END -->",
            "<!-- RECENT_RELEASES:START -->",
            "<!-- RECENT_RELEASES:END -->"
        ]
        for marker in markers:
            self.assertIn(marker, self.content, f"Missing essential HTML comment marker: '{marker}'")

    def test_verified_credentials_accuracy(self):
        # Must accurately denote CCNA as coursework / training completion, not official Cisco certification
        self.assertIn("CCNA", self.content)
        self.assertIn("training", self.content.lower())
        # Must not claim confirmed employment or completed CEH certification
        self.assertNotIn("CEH certified", self.content.lower())
        self.assertNotIn("cisco certified network associate certified", self.content.lower())

    def test_markdown_links_format(self):
        # Verify that all markdown links have valid brackets and urls
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', self.content)
        self.assertGreater(len(links), 5)
        for label, url in links:
            self.assertTrue(url.startswith("http://") or url.startswith("https://") or url.startswith("#"),
                            f"Suspicious link URL format: {url} with label {label}")

if __name__ == "__main__":
    unittest.main()

