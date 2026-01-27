"""Queued interaction system for deferred actions."""


class QueuedInteraction:
    """Represents an interaction that will be executed when the player reaches the target."""

    def __init__(self, target, action_callable, args=(), description=""):
        self.target = target
        self.action_callable = action_callable
        self.args = args
        self.description = description

    def __repr__(self):
        return f"QueuedInteraction({self.description or self.action_callable.__name__})"
