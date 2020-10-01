from pathlib import Path

import pytest


@pytest.fixture()
def fixtures_dir(pytestconfig):
    return Path(pytestconfig.rootdir, "test", "fixtures")
