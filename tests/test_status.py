"""Tests for the Status enum used by polling logic."""
from nodes.status import Status


def test_all_expected_statuses_exist():
    assert Status.READY.value == "Ready"
    assert Status.PENDING.value == "Pending"
    assert Status.ERROR.value == "Error"
    assert Status.CONTENT_MODERATED.value == "Content Moderated"
    assert Status.REQUEST_MODERATED.value == "Request Moderated"
    assert Status.TASK_NOT_FOUND.value == "Task not found"


def test_status_from_string():
    assert Status("Ready") == Status.READY
    assert Status("Pending") == Status.PENDING
    assert Status("Error") == Status.ERROR


def test_terminal_statuses_are_distinct_from_pending():
    terminal = {Status.ERROR, Status.CONTENT_MODERATED, Status.REQUEST_MODERATED}
    assert Status.PENDING not in terminal
    assert Status.READY not in terminal
