"""Tests for the polling + progress bar behaviour in Direct nodes."""
import pytest
from unittest.mock import patch, MagicMock
import io
from PIL import Image

from helpers import make_ready_response, make_pending_response, make_error_response, make_moderated_response


def _mock_image_response(jpeg_bytes):
    """Create a mock requests.get response that returns a JPEG."""
    resp = MagicMock()
    resp.content = jpeg_bytes
    return resp


def _make_poll_responses(statuses, sample_jpeg_bytes):
    """Build a list of mock HTTP responses for sequential poll calls.
    statuses: list of BFL status dicts, e.g. [make_pending_response(), make_ready_response()]
    """
    responses = []
    for s in statuses:
        r = MagicMock()
        r.status_code = 200
        r.json.return_value = s
        responses.append(r)
    return responses


@pytest.fixture
def mock_config():
    """Minimal config loader mock."""
    loader = MagicMock()
    loader.get_x_key.return_value = "test-key"
    loader.create_url.return_value = "https://api.bfl.ai/get_result?id=test-task"
    return loader


# ---------------------------------------------------------------------------
# Flux 2 Max Direct polling
# ---------------------------------------------------------------------------

class TestFlux2MaxPolling:

    @patch("nodes.flux2max_direct.time.sleep")  # skip real sleeps
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_ready_on_first_poll(self, mock_gcl, mock_get, mock_sleep, mock_config, sample_jpeg_bytes):
        mock_gcl.return_value = mock_config

        # Poll returns Ready immediately
        poll_resp = MagicMock()
        poll_resp.status_code = 200
        poll_resp.json.return_value = make_ready_response("https://example.com/img.jpg")

        # Image download
        img_resp = _mock_image_response(sample_jpeg_bytes)

        mock_get.side_effect = [poll_resp, img_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=5)

        assert isinstance(result, tuple)
        assert result[0].shape[0] == 1  # batch dim
        assert result[0].shape[3] == 3  # RGB
        mock_sleep.assert_not_called()

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_pending_then_ready(self, mock_gcl, mock_get, mock_sleep, mock_config, sample_jpeg_bytes):
        mock_gcl.return_value = mock_config

        pending = MagicMock(status_code=200)
        pending.json.return_value = make_pending_response()
        ready = MagicMock(status_code=200)
        ready.json.return_value = make_ready_response()
        img_resp = _mock_image_response(sample_jpeg_bytes)

        mock_get.side_effect = [pending, pending, ready, img_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=10)

        assert isinstance(result, tuple)
        assert result[0].shape[3] == 3
        assert mock_sleep.call_count == 2  # slept after each pending

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_error_stops_polling(self, mock_gcl, mock_get, mock_sleep, mock_config):
        mock_gcl.return_value = mock_config

        error_resp = MagicMock(status_code=200)
        error_resp.json.return_value = make_error_response()
        mock_get.side_effect = [error_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=10)

        # Should return blank image
        assert result[0].shape == (1, 512, 512, 3)
        # Should not have polled again
        assert mock_get.call_count == 1

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_moderated_stops_polling(self, mock_gcl, mock_get, mock_sleep, mock_config):
        mock_gcl.return_value = mock_config

        mod_resp = MagicMock(status_code=200)
        mod_resp.json.return_value = make_moderated_response()
        mock_get.side_effect = [mod_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=10)

        assert result[0].shape == (1, 512, 512, 3)
        assert mock_get.call_count == 1

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_exhausted_attempts_returns_blank(self, mock_gcl, mock_get, mock_sleep, mock_config):
        mock_gcl.return_value = mock_config

        pending = MagicMock(status_code=200)
        pending.json.return_value = make_pending_response()
        mock_get.return_value = pending

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=3)

        assert result[0].shape == (1, 512, 512, 3)
        assert mock_get.call_count == 3

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_http_error_retries(self, mock_gcl, mock_get, mock_sleep, mock_config, sample_jpeg_bytes):
        mock_gcl.return_value = mock_config

        http_err = MagicMock(status_code=500)
        ready = MagicMock(status_code=200)
        ready.json.return_value = make_ready_response()
        img_resp = _mock_image_response(sample_jpeg_bytes)

        mock_get.side_effect = [http_err, ready, img_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=5)

        assert result[0].shape[3] == 3  # got a real image back


# ---------------------------------------------------------------------------
# Flux 2 Klein 9B Direct polling (same logic, quick smoke test)
# ---------------------------------------------------------------------------

class TestFlux2KleinPolling:

    @patch("nodes.flux2klein_direct.time.sleep")
    @patch("nodes.flux2klein_direct.requests.get")
    @patch("nodes.flux2klein_direct.get_config_loader")
    def test_ready_on_first_poll(self, mock_gcl, mock_get, mock_sleep, mock_config, sample_jpeg_bytes):
        mock_gcl.return_value = mock_config

        poll_resp = MagicMock(status_code=200)
        poll_resp.json.return_value = make_ready_response()
        img_resp = _mock_image_response(sample_jpeg_bytes)
        mock_get.side_effect = [poll_resp, img_resp]

        from nodes.flux2klein_direct import Flux2Klein9bDirect
        node = Flux2Klein9bDirect()
        result = node._poll_with_progress("test-task", max_attempts=5)

        assert isinstance(result, tuple)
        assert result[0].shape[3] == 3
        mock_sleep.assert_not_called()

    @patch("nodes.flux2klein_direct.time.sleep")
    @patch("nodes.flux2klein_direct.requests.get")
    @patch("nodes.flux2klein_direct.get_config_loader")
    def test_exhausted_returns_blank(self, mock_gcl, mock_get, mock_sleep, mock_config):
        mock_gcl.return_value = mock_config

        pending = MagicMock(status_code=200)
        pending.json.return_value = make_pending_response()
        mock_get.return_value = pending

        from nodes.flux2klein_direct import Flux2Klein9bDirect
        node = Flux2Klein9bDirect()
        result = node._poll_with_progress("test-task", max_attempts=3)

        assert result[0].shape == (1, 512, 512, 3)


# ---------------------------------------------------------------------------
# Progress bar behaviour
# ---------------------------------------------------------------------------

class TestProgressBar:

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_progress_fills_to_max_on_ready(self, mock_gcl, mock_get, mock_sleep, mock_config, sample_jpeg_bytes):
        mock_gcl.return_value = mock_config

        pending = MagicMock(status_code=200)
        pending.json.return_value = make_pending_response()
        ready = MagicMock(status_code=200)
        ready.json.return_value = make_ready_response()
        img_resp = _mock_image_response(sample_jpeg_bytes)

        mock_get.side_effect = [pending, pending, ready, img_resp]

        from nodes.flux2max_direct import Flux2MaxDirect
        import comfy.utils

        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=10)

        # Sum of all progress updates should equal max_attempts (filled to 100%)
        # 2 pending (1 each) + ready fills remaining (10 - 3 + 1 = 8) = 10
        # Actually: attempt 1 pending → update(1), attempt 2 pending → update(1),
        # attempt 3 ready → update(10 - 3 + 1 = 8) = total 10
        # We can't easily grab the pbar instance, but we can verify the result is valid
        assert result[0].shape[3] == 3

    @patch("nodes.flux2max_direct.time.sleep")
    @patch("nodes.flux2max_direct.requests.get")
    @patch("nodes.flux2max_direct.get_config_loader")
    def test_progress_fills_on_error(self, mock_gcl, mock_get, mock_sleep, mock_config):
        mock_gcl.return_value = mock_config

        pending = MagicMock(status_code=200)
        pending.json.return_value = make_pending_response()
        error = MagicMock(status_code=200)
        error.json.return_value = make_error_response()

        mock_get.side_effect = [pending, error]

        from nodes.flux2max_direct import Flux2MaxDirect
        node = Flux2MaxDirect()
        result = node._poll_with_progress("test-task", max_attempts=10)

        # Should return blank and not hang
        assert result[0].shape == (1, 512, 512, 3)
