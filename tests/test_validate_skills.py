import pathlib, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skills import validate  # noqa: E402


def make(root, name, body):
    d = pathlib.Path(root) / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(body)


class ValidatorTest(unittest.TestCase):
    def test_repo_is_valid(self):
        n, errs = validate(ROOT)
        self.assertEqual(errs, [])
        self.assertEqual(n, 5)

    def test_good_skill(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "---\nname: demo\ndescription: A long enough description here\n---\n# Demo\n")
            self.assertEqual(validate(t), (1, []))

    def test_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "# no frontmatter\n")
            self.assertIn("missing frontmatter", validate(t)[1][0])

    def test_name_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "---\nname: other\ndescription: A long enough description here\n---\n")
            self.assertIn("name must equal folder", validate(t)[1][0])

    def test_short_description(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "---\nname: demo\ndescription: short\n---\n")
            self.assertIn("description too short", validate(t)[1][0])

    def test_banned_reference(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "---\nname: demo\ndescription: A long enough description here\n---\nsee /Users/someone/x\n")
            self.assertTrue(any("banned" in e for e in validate(t)[1]))

    def test_secret_pattern(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, "demo", "---\nname: demo\ndescription: A long enough description here\n---\nkey " + "gh" + "p_abc123\n")
            self.assertTrue(any("banned" in e for e in validate(t)[1]))


if __name__ == "__main__":
    unittest.main()
