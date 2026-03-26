"""Ouroboros Supervisor package — decomposed from monolithic colab_launcher.py."""

from .supervisor import Supervisor
from .config import SupervisorConfig
from .state import SupervisorState
from .event_bus import EventBus
from .worker_pool import WorkerPool

# For backward compatibility, expose core types at package level
__all__ = [
    "Supervisor",
    "SupervisorConfig",
    "SupervisorState",
    "EventBus",
    "WorkerPool"
]