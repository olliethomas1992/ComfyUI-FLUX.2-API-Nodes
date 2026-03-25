"""Shared test helpers and factory functions."""
import torch
from PIL import Image
import io


def make_image_tensor(width=64, height=64):
    """Create a minimal ComfyUI-style IMAGE tensor (1, H, W, 3) float32 0-1."""
    return torch.rand(1, height, width, 3, dtype=torch.float32)


def make_ready_response(sample_url="https://example.com/image.jpg"):
    return {"status": "Ready", "result": {"sample": sample_url}}


def make_pending_response():
    return {"status": "Pending"}


def make_error_response():
    return {"status": "Error"}


def make_moderated_response():
    return {"status": "Content Moderated"}


def make_sample_jpeg_bytes():
    img = Image.new("RGB", (4, 4), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()
