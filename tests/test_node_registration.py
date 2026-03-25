"""Tests that node classes are properly structured for ComfyUI registration."""
import pytest


def test_flux2max_direct_has_required_attrs():
    from nodes.flux2max_direct import Flux2MaxDirect, NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

    assert "Flux2MaxDirect_BFL" in NODE_CLASS_MAPPINGS
    assert NODE_CLASS_MAPPINGS["Flux2MaxDirect_BFL"] is Flux2MaxDirect
    assert "Flux2MaxDirect_BFL" in NODE_DISPLAY_NAME_MAPPINGS

    # ComfyUI required class attributes
    assert Flux2MaxDirect.RETURN_TYPES == ("IMAGE",)
    assert Flux2MaxDirect.FUNCTION == "generate_image"
    assert Flux2MaxDirect.CATEGORY == "BFL/Flux2"


def test_flux2klein_direct_has_required_attrs():
    from nodes.flux2klein_direct import Flux2Klein9bDirect, NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

    assert "Flux2Klein9bDirect_BFL" in NODE_CLASS_MAPPINGS
    assert NODE_CLASS_MAPPINGS["Flux2Klein9bDirect_BFL"] is Flux2Klein9bDirect
    assert "Flux2Klein9bDirect_BFL" in NODE_DISPLAY_NAME_MAPPINGS

    assert Flux2Klein9bDirect.RETURN_TYPES == ("IMAGE",)
    assert Flux2Klein9bDirect.FUNCTION == "generate_image"
    assert Flux2Klein9bDirect.CATEGORY == "BFL/Flux2"


def test_flux2max_input_types_structure():
    from nodes.flux2max_direct import Flux2MaxDirect

    inputs = Flux2MaxDirect.INPUT_TYPES()
    assert "required" in inputs
    assert "optional" in inputs

    # Required fields
    assert "prompt" in inputs["required"]
    assert "safety_tolerance" in inputs["required"]
    assert "output_format" in inputs["required"]

    # Should have 8 image slots
    for i in range(1, 9):
        assert f"image_{i}" in inputs["optional"]


def test_flux2klein_input_types_structure():
    from nodes.flux2klein_direct import Flux2Klein9bDirect

    inputs = Flux2Klein9bDirect.INPUT_TYPES()
    assert "required" in inputs
    assert "optional" in inputs

    # Should have 4 image slots (not 8)
    for i in range(1, 5):
        assert f"image_{i}" in inputs["optional"]
    assert "image_5" not in inputs["optional"]


def test_flux2max_has_config_input():
    from nodes.flux2max_direct import Flux2MaxDirect

    inputs = Flux2MaxDirect.INPUT_TYPES()
    assert "config" in inputs["optional"]
    assert inputs["optional"]["config"] == ("BFL_CONFIG",)


def test_flux2klein_has_config_input():
    from nodes.flux2klein_direct import Flux2Klein9bDirect

    inputs = Flux2Klein9bDirect.INPUT_TYPES()
    assert "config" in inputs["optional"]
    assert inputs["optional"]["config"] == ("BFL_CONFIG",)
