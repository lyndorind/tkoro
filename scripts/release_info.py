
import os
import re
import tomllib
from pathlib import Path

with open("pyproject.toml", "rb") as file:
    project = tomllib.load(file)

version = project["project"]["version"]

if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise ValueError(f"Expected SemVer version, got: {version}")

changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

pattern = (
    r"^##\s+\[?" + re.escape(version)
    + r"\]?(?:\s*[-–]\s*[^\n]+)?\s*$"
)

match = re.search(pattern, changelog, flags=re.MULTILINE)

if not match:
    raise ValueError(
        f"Version {version} not found in CHANGELOG.md"
    )

rest = changelog[match.end():]
next_heading = re.search(r"^##\s+", rest, flags=re.MULTILINE)

if next_heading:
    notes = rest[:next_heading.start()].strip()
else:
    notes = rest.strip()

if not notes:
    raise ValueError("Release notes section is empty")

Path("release_notes.md").write_text(
    notes + "\n", encoding="utf-8"
)

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as file:
    file.write(f"version={version}\n")

print(f"Prepared release v{version}")
print(notes)
