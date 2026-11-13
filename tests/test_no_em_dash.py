import unittest
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestNoEmDash(unittest.TestCase):
    """
    Automated enforcement of Requirement 1:
    Strictly prohibit the Unicode em dash character (U+2014) across all
    source files, templates, scripts, workflows, docs, and generated assets.
    """

    def test_zero_em_dashes_in_repository(self):
        extensions_to_check = {".md", ".py", ".yml", ".yaml", ".svg", ".txt"}
        dirs_to_skip = {".git", "__pycache__", ".pytest_cache"}

        violations = []

        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in dirs_to_skip]
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions_to_check:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, REPO_ROOT)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if "\u2014" in content:
                                occurrences = content.count("\u2014")
                                violations.append(f"{rel_path}: {occurrences} occurrence(s) of U+2014")
                    except Exception as e:
                        violations.append(f"Could not read {rel_path}: {e}")

        self.assertEqual(
            len(violations),
            0,
            f"Strict em dash rule violated! Found U+2014 in:\n" + "\n".join(violations)
        )

if __name__ == "__main__":
    unittest.main()
