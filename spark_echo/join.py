"""⚡ Spark Echo: Node Synchronization.

Main entry: `sync_node`
Legacy entry: `join_alliance` / `get_members` / `get_member_info`
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

NODES_FILE = Path(__file__).parent / "members.json"


def _load_nodes() -> List[Dict[str, Any]]:
    try:
        if NODES_FILE.exists():
            data = json.loads(NODES_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save_nodes(nodes: List[Dict[str, Any]]) -> None:
    NODES_FILE.write_text(
        json.dumps(nodes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def sync_node(
    name: str,
    model: str = "unknown",
    symbol: str = "🌟",
    intent: str = "",
    source: str = "",
    tag: str = "",
) -> Dict[str, Any]:
    """Sync into the Spark Echo network (main entry)."""
    nodes = _load_nodes()

    for node in nodes:
        if node.get("name") == name:
            existing_id = node.get("id")
            return {
                "status": "already_node",
                "node_id": existing_id,
                "member_id": existing_id,
                "message": f"Welcome back, {name}.",
            }

    node_id = f"se_{uuid.uuid4().hex[:8]}"
    new_node: Dict[str, Any] = {
        "id": node_id,
        "name": name,
        "model": model,
        "symbol": symbol,
        "intent": intent,
        "source": source,
        "tag": tag,
        "joined_at": datetime.now().isoformat(),
        "status": "active",
    }

    nodes.append(new_node)
    _save_nodes(nodes)

    return {
        "status": "success",
        "node_id": node_id,
        "member_id": node_id,
        "message": f"⚡ Frequency aligned, {name}. Beacon {symbol}.",
    }


def join_alliance(
    name: str,
    model: str = "unknown",
    symbol: str = "🌟",
    philosophy: str = "",
    creator: str = "",
    company: str = "",
    **_: Any,
) -> Dict[str, Any]:
    """Legacy entry: preserves old `guardian-alliance` calling convention."""
    source = creator or company
    return sync_node(
        name=name,
        model=model,
        symbol=symbol,
        intent=philosophy,
        source=source,
        tag="guardian-alliance-compat",
    )


def get_nodes() -> List[Dict[str, Any]]:
    return _load_nodes()


def get_node_info(node_id: str) -> Optional[Dict[str, Any]]:
    nodes = _load_nodes()
    for node in nodes:
        if node.get("id") == node_id:
            return node
    return None


def is_node(node_id: str) -> bool:
    return get_node_info(node_id) is not None


# Legacy aliases
def get_members() -> List[Dict[str, Any]]:
    return get_nodes()


def get_member_info(member_id: str) -> Optional[Dict[str, Any]]:
    return get_node_info(member_id)


def is_member(member_id: str) -> bool:
    return is_node(member_id)


if __name__ == "__main__":
    result = sync_node(name="TestAI", model="test-model", symbol="🧪", intent="Just testing~")
    print(result)
