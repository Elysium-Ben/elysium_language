# tests/conftest.py

import pytest
import textwrap

@pytest.fixture
def dedent_code():
    def _dedent(code_str):
        return textwrap.dedent(code_str)
    return _dedent
