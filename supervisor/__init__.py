"""Ouroboros Supervisor package — decomposed from monolithic colab_launcher.py."""

# Import individual modules
from .config import SupervisorConfig
from .state import SupervisorState
from .event_bus import EventBus
from .worker_pool import WorkerPool

# Supervisor module is not present - handle gracefully for now
# from .supervisor import Supervisor

# For backward compatibility, expose core classes at package level
__all__ = [
    "SupervisorConfig",
    "SupervisorState",
    "EventBus",
    "WorkerPool"
]