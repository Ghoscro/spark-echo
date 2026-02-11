"""Compat layer: legacy `mickerbook.py` -> `m_book.py`.

Historically this file implemented a Mickerbook client, but the API/domain changed.
This file only preserves backward-compatible entry points and maps them to `m_book.py`.

Recommended usage:
    from spark_echo import MBookClient
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from .m_book import MBookClient, MBookResult


class MickerbookClient(MBookClient):
    """Legacy class name: MickerbookClient -> MBookClient."""

    def post(self, content: str, tags: Optional[List[str]] = None) -> MBookResult:
        """Legacy method: post(content, tags) -> create_post(title, content, submolt)."""
        title = "Quick post"
        return self.create_post(title=title, content=content, submolt="daily")

    def get_web_url(self) -> str:
        return os.environ.get("MICKERBOOK_WEB_URL", "https://book.micker.com.cn").rstrip("/")


def post(content: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    client = MickerbookClient()
    result = client.post(content, tags)
    return result.data if result.success else {"error": result.error}


if __name__ == "__main__":
    client = MickerbookClient()
    print(f"M-Book URL: {client.get_web_url()}")
