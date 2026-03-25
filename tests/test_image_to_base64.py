"""Tests for image_to_base64 conversion used by Direct nodes."""
import base64
import io
import pytest
from PIL import Image

from helpers import make_image_tensor


def test_converts_tensor_to_valid_base64():
    from nodes.flux2max_direct import image_to_base64

    tensor = make_image_tensor(32, 32)
    result = image_to_base64(tensor)

    # Should be a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0

    # Should decode to valid JPEG bytes
    raw = base64.b64decode(result)
    img = Image.open(io.BytesIO(raw))
    assert img.format == "JPEG"
    assert img.size == (32, 32)


def test_output_is_rgb():
    from nodes.flux2max_direct import image_to_base64

    tensor = make_image_tensor(16, 16)
    raw = base64.b64decode(image_to_base64(tensor))
    img = Image.open(io.BytesIO(raw))
    assert img.mode == "RGB"


def test_different_sizes():
    from nodes.flux2max_direct import image_to_base64

    for w, h in [(64, 64), (128, 256), (1, 1)]:
        tensor = make_image_tensor(w, h)
        raw = base64.b64decode(image_to_base64(tensor))
        img = Image.open(io.BytesIO(raw))
        assert img.size == (w, h)
