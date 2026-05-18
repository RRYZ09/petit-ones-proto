from typing import Protocol


class Body(Protocol):
    def read_state(self) -> dict:
        """Read current body state."""

    def write_state(self, state: dict) -> None:
        """Persist body state."""
