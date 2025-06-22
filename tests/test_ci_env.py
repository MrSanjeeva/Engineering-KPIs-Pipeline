"""
Quick sanity‑check run in CI.

Fails fast if the required secrets are not injected into the
GitHub Actions runner.  This prevents the ingest refresh step
from blowing up with a less helpful stack‑trace later on.
"""

import os
import pytest

REQUIRED_VARS = ("GH_PAT", "JIRA_TOKEN")


@pytest.mark.parametrize("var", REQUIRED_VARS)
def test_required_env_vars_present(var: str) -> None:
    """Ensure every secret the pipeline needs is available in the runner."""
    assert os.getenv(var), f"Missing required CI secret: {var}"
