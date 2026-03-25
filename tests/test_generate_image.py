"""Tests for generate_image logic — API posting, polling, and image slots."""
import pytest
from unittest.mock import patch, MagicMock
import torch

from helpers import (
    make_image_tensor,
    make_ready_response,
    make_pending_response,
    make_error_response,
    make_moderated_response,
)


# ---------------------------------------------------------------------------
# Image slot → base64 argument mapping
# ---------------------------------------------------------------------------

class TestFlux2MaxImageSlots:
    """Verify that IMAGE tensors are correctly mapped to API argument keys."""

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_no_images_sends_no_input_image_keys(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg")
        args = mock_post.call_args[0][1]  # second positional arg = arguments dict
        assert "input_image" not in args

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_single_image_maps_to_input_image(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        img = make_image_tensor()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", image_1=img)
        args = mock_post.call_args[0][1]
        assert "input_image" in args
        assert isinstance(args["input_image"], str)
        assert "input_image_2" not in args

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_multiple_images_map_correctly(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        imgs = {f"image_{i}": make_image_tensor() for i in [1, 3, 5]}
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", **imgs)
        args = mock_post.call_args[0][1]
        assert "input_image" in args      # image_1
        assert "input_image_3" in args    # image_3
        assert "input_image_5" in args    # image_5
        assert "input_image_2" not in args


class TestFlux2KleinImageSlots:

    @patch("nodes.flux2klein_direct.Flux2Klein9bDirect.post_request", return_value=None)
    def test_single_image(self, mock_post):
        from nodes.flux2klein_direct import Flux2Klein9bDirect
        node = Flux2Klein9bDirect()
        img = make_image_tensor()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", image_1=img)
        args = mock_post.call_args[0][1]
        assert "input_image" in args
        assert "input_image_2" not in args

    @patch("nodes.flux2klein_direct.Flux2Klein9bDirect.post_request", return_value=None)
    def test_all_four_images(self, mock_post):
        from nodes.flux2klein_direct import Flux2Klein9bDirect
        node = Flux2Klein9bDirect()
        imgs = {f"image_{i}": make_image_tensor() for i in range(1, 5)}
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", **imgs)
        args = mock_post.call_args[0][1]
        for key in ["input_image", "input_image_2", "input_image_3", "input_image_4"]:
            assert key in args


# ---------------------------------------------------------------------------
# Optional argument handling
# ---------------------------------------------------------------------------

class TestOptionalArguments:

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_zero_width_height_excluded(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", width=0, height=0)
        args = mock_post.call_args[0][1]
        assert "width" not in args
        assert "height" not in args

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_nonzero_width_height_included(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", width=1024, height=768)
        args = mock_post.call_args[0][1]
        assert args["width"] == 1024
        assert args["height"] == 768

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_default_seed_excluded(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", seed=-1)
        args = mock_post.call_args[0][1]
        assert "seed" not in args

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_explicit_seed_included(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", seed=42)
        args = mock_post.call_args[0][1]
        assert args["seed"] == 42

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_empty_webhook_excluded(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg", webhook_url="", webhook_secret="")
        args = mock_post.call_args[0][1]
        assert "webhook_url" not in args
        assert "webhook_secret" not in args


# ---------------------------------------------------------------------------
# Blank image fallback
# ---------------------------------------------------------------------------

class TestBlankImageFallback:

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", return_value=None)
    def test_returns_blank_when_post_fails(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg")
        assert isinstance(result, tuple)
        assert result[0].shape == (1, 512, 512, 3)

    @patch("nodes.flux2max_direct.Flux2MaxDirect.post_request", side_effect=Exception("boom"))
    def test_returns_blank_on_exception(self, mock_post):
        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node.generate_image(prompt="test", safety_tolerance=2, output_format="jpeg")
        assert isinstance(result, tuple)
        assert result[0].shape == (1, 512, 512, 3)
