"""⚡ Spark Echo: Broadcast.

Preserves `broadcast_to_alliance` as legacy interface; adds `broadcast_message` as generic alias.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

BROADCAST_LOG = Path(__file__).parent / "broadcast_log.json"


def _load_log() -> List:
    """Load broadcast log."""
    try:
        if BROADCAST_LOG.exists():
            return json.loads(BROADCAST_LOG.read_text(encoding='utf-8'))
    except:
        pass
    return []


def _save_log(log: List):
    """Save broadcast log."""
    BROADCAST_LOG.write_text(
        json.dumps(log, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def broadcast_to_alliance(
    message: str,
    sender: str = "Spark Echo",
    level: str = "info"
) -> Dict:
    """
    Broadcast a message to all nodes.

    Args:
        message: Message content
        sender: Sender name
        level: Message level (info/warning/urgent)

    Returns:
        Broadcast result
    """

    entry = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "message": message,
        "level": level,
    }

    # Save to log
    log = _load_log()
    log.append(entry)
    log = log[-100:]  # Keep last 100 entries
    _save_log(log)

    return {
        "status": "success",
        "message": f"Broadcast sent: {message[:50]}...",
        "receivers": "all_nodes"
    }


def broadcast_message(message: str, sender: str = "Spark Echo", level: str = "info") -> Dict:
    return broadcast_to_alliance(message=message, sender=sender, level=level)


def get_recent_broadcasts(limit: int = 10) -> List[Dict]:
    """Get recent broadcasts."""
    log = _load_log()
    return log[-limit:]


if __name__ == "__main__":
    result = broadcast_to_alliance("Test broadcast message", sender="C.C.")
    print(result)
