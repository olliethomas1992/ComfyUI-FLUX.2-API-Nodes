"""Shared fixtures and stubs for BFL node tests."""
import sys
import os
import types

# --- Path setup ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO_ROOT)
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

# --- Stub comfy.utils before any node imports ---
comfy_module = types.ModuleType("comfy")
comfy_utils = types.ModuleType("comfy.utils")


class FakeProgressBar:
    def __init__(self, total):
        self.total = total
        self.updates = []

    def update(self, value):
        self.updates.append(value)


comfy_utils.ProgressBar = FakeProgressBar
comfy_module.utils = comfy_utils
sys.modules["comfy"] = comfy_module
sys.modules["comfy.utils"] = comfy_utils

# --- Pre-import the node submodules so @patch targets resolve ---
import nodes.flux2max_direct  # noqa: E402
import nodes.flux2klein_direct  # noqa: E402

# --- Fixtures ---
import pytest  # noqa: E402
from helpers import make_image_tensor, make_sample_jpeg_bytes  # noqa: E402


@pytest.fixture
def dummy_image():
    return make_image_tensor()


@pytest.fixture
def sample_jpeg_bytes():
    return make_sample_jpeg_bytes()
