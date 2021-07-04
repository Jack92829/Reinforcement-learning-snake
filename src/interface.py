import logging

# from environment import _Environment

logger = logging.getLogger(__name__)


class Environment:
    _valid_parameters = {
        "on_ready": [],
        "on_action": ["state"],
        "on_step": ["state", "reward", "action", "next_state", "terminal"],
        "on_reset": ["kwargs"],
        "on_finish": ["kwargs"]
    }
    _valid_events = [
        "on_ready",
        "on_action",
        "on_step",
        "on_reset",
        "on_finish"
    ]

    def __init__(self) -> None:
        ...
