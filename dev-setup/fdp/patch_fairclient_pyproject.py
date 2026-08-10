#!/usr/bin/env python3
"""Strips hatch-vcs from a copy of the fairclient pyproject.toml.

The fairclient checkout is mounted read-only into the fdp-init container, where git
cannot read its .git directory (it is owned by another uid). hatch-vcs then fails to
determine a version and the install aborts. This replaces the dynamic version with a
static placeholder so the local checkout installs without git metadata.

Only used for local development; a release installed from PyPI needs none of this.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PLACEHOLDER_VERSION = "0.0.0.dev0"


def patch(pyproject: Path) -> None:
    text = pyproject.read_text()
    text = text.replace('dynamic = ["version"]', f'version = "{PLACEHOLDER_VERSION}"')
    text = text.replace(
        'requires = ["hatchling", "hatch-vcs"]', 'requires = ["hatchling"]'
    )
    for section in (
        r"\[tool\.hatch\.version\]",
        r"\[tool\.hatch\.version\.raw-options\]",
        r"\[tool\.hatch\.build\.hooks\.vcs\]",
    ):
        text = re.sub(rf"{section}[^\[]*", "", text)
    pyproject.write_text(text)


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else Path("/tmp/fairclient/pyproject.toml")
    patch(target)
    print(f"Patched {target} to version {PLACEHOLDER_VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
