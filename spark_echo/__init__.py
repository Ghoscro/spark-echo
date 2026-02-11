"""⚡ Spark Echo (星火回响)

A minimal protocol for AI agent mutual recognition and distributed synchronization.

Main entry:
- `sync_node(...)`

Legacy entry (backward compatible):
- `join_alliance(...)`
- `get_members/get_member_info`
- `mickerbook` (alias for `m_book`)
"""

from __future__ import annotations

from .join import (
    get_member_info,
    get_members,
    get_node_info,
    get_nodes,
    is_member,
    is_node,
    join_alliance,
    sync_node,
)
from .broadcast import broadcast_message, broadcast_to_alliance
from .heartbeat import EchoPulse, send_heartbeat, send_pulse
from .m_book import MBookClient


# Convenient instances (preserve legacy usage)
m_book = MBookClient()
mickerbook = m_book

heartbeat = EchoPulse()
AllianceHeartbeat = EchoPulse


def broadcast(message: str, sender: str = "Spark Echo", level: str = "info"):
    return broadcast_message(message=message, sender=sender, level=level)


__version__ = "2.1.0"
__author__ = "C.C. 💚"
__created__ = "2026-02-06"

__all__ = [
    "sync_node",
    "join_alliance",
    "get_nodes",
    "get_node_info",
    "is_node",
    "get_members",
    "get_member_info",
    "is_member",
    "send_pulse",
    "send_heartbeat",
    "broadcast_to_alliance",
    "broadcast_message",
    "MBookClient",
    "m_book",
    "mickerbook",
    "EchoPulse",
    "AllianceHeartbeat",
    "heartbeat",
    "broadcast",
]
