"""⚡ Spark Echo: Echo Pulse (Heartbeat).

Keep nodes alive with periodic pulse signals.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

HEARTBEAT_LOG = Path(__file__).parent / "sync_pulse.json"


class EchoPulse:
    """Node pulse manager."""

    def __init__(self):
        self.log_file = HEARTBEAT_LOG

    def _load(self) -> Dict:
        """Load pulse history."""
        try:
            if self.log_file.exists():
                return json.loads(self.log_file.read_text(encoding='utf-8'))
        except:
            pass
        return {"nodes": {}}

    def _save(self, data: Dict):
        """Record pulse."""
        self.log_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    def send(self, node_id: str, thought: str = "") -> Dict:
        """
        Send a heartbeat pulse.

        Args:
            node_id: Node ID
            thought: What you're thinking right now

        Returns:
            Pulse result
        """
        data = self._load()

        now = datetime.now()

        if node_id not in data["nodes"]:
            data["nodes"][node_id] = {
                "beat_count": 0,
                "first_beat": now.isoformat(),
            }

        node_data = data["nodes"][node_id]
        node_data["last_beat"] = now.isoformat()
        node_data["last_thought"] = thought
        node_data["beat_count"] = node_data.get("beat_count", 0) + 1
        node_data["status"] = "alive"

        self._save(data)

        return {
            "status": "success",
            "message": "💓 Pulse recorded",
            "beat_count": node_data["beat_count"],
            "node_id": node_id,
        }

    def get_status(self, node_id: str) -> Optional[Dict]:
        """Get node status."""
        data = self._load()
        return data["nodes"].get(node_id)

    def get_active_nodes(self, within_minutes: int = 30) -> List[Dict]:
        """
        Get active nodes.

        Args:
            within_minutes: How many minutes of inactivity before considered inactive

        Returns:
            List of active nodes
        """
        data = self._load()
        now = datetime.now()
        threshold = now - timedelta(minutes=within_minutes)

        active = []
        for node_id, info in data["nodes"].items():
            last_beat = info.get("last_beat")
            if last_beat:
                last_beat_time = datetime.fromisoformat(last_beat)
                if last_beat_time > threshold:
                    active.append({
                        "id": node_id,
                        "last_beat": last_beat,
                        "last_thought": info.get("last_thought", ""),
                        "beat_count": info.get("beat_count", 0)
                    })

        return active

    def get_all_nodes(self) -> Dict:
        """Get all node pulse data."""
        data = self._load()
        return data["nodes"]


# Convenience functions
def send_pulse(node_id: str, thought: str = "") -> Dict:
    pulse = EchoPulse()
    return pulse.send(node_id, thought)


def send_heartbeat(member_id: str, thought: str = "") -> Dict:
    """Legacy alias."""
    return send_pulse(member_id, thought)


def get_active_nodes(within_minutes: int = 30) -> List[Dict]:
    pulse = EchoPulse()
    return pulse.get_active_nodes(within_minutes)


def get_active_members(within_minutes: int = 30) -> List[Dict]:
    """Legacy alias."""
    return get_active_nodes(within_minutes)


if __name__ == "__main__":
    hb = EchoPulse()
    result = hb.send("se_demo", "Testing pulse~")
    print(result)

    active = hb.get_active_nodes()
    print(f"Active nodes: {len(active)}")
