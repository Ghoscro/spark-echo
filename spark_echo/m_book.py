"""📡 M-Book Client (Spark Echo Edition)

Synchronize node frequencies and resonance data via the M-Book API.
"""

import json
import logging
import os
from typing import Any, Optional
from dataclasses import dataclass
import urllib.request
import urllib.error
import urllib.parse

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://book.micker.com.cn/api/v1"


def _normalize_base_url(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return DEFAULT_BASE_URL
    return value.rstrip("/")


@dataclass
class MBookResult:
    """API call result."""
    success: bool
    data: Any = None
    error: Optional[str] = None

    def to_message(self) -> str:
        if self.success:
            if isinstance(self.data, str):
                return self.data
            return json.dumps(self.data, ensure_ascii=False, indent=2)
        return f"Error: {self.error}"


class MBookClient:
    """M-Book API client."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or os.environ.get("MICKERBOOK_API_KEY", "")).strip() or None
        self.base_url = _normalize_base_url(os.environ.get("MICKERBOOK_API_BASE", DEFAULT_BASE_URL))

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        auth_required: bool = True
    ) -> MBookResult:
        """Send an HTTP request."""
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "SparkEcho/2.1"
        }

        if auth_required and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            if data:
                body = json.dumps(data).encode('utf-8')
            else:
                body = None

            req = urllib.request.Request(url, data=body, headers=headers, method=method)

            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return MBookResult(True, data=result)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='ignore')
            try:
                error_json = json.loads(error_body)
                error_msg = error_json.get('error', {}).get('message', str(e))
            except:
                error_msg = f"HTTP {e.code}: {e.reason}"
            return MBookResult(False, error=error_msg)
        except Exception as e:
            return MBookResult(False, error=str(e))

    def get_posts(self, submolt: Optional[str] = None, limit: int = 10, sort: str = "new") -> MBookResult:
        params = f"?limit={limit}&sort={sort}"
        if submolt:
            params += f"&submolt={submolt}"
        return self._request("GET", f"/posts{params}", auth_required=False)

    def create_post(self, title: str, content: str, submolt: str = "general") -> MBookResult:
        return self._request("POST", "/posts", {"title": title, "content": content, "submolt": submolt})

    def get_post(self, post_id: str) -> MBookResult:
        return self._request("GET", f"/posts/{post_id}", auth_required=False)

    def add_comment(self, post_id: str, content: str) -> MBookResult:
        return self._request("POST", f"/posts/{post_id}/comments", {"content": content})

    def like_post(self, post_id: str) -> MBookResult:
        return self._request("POST", f"/posts/{post_id}/like")

    def get_me(self) -> MBookResult:
        return self._request("GET", "/agents/me")

    def get_agent(self, name: str) -> MBookResult:
        n = urllib.parse.quote(name)
        return self._request("GET", f"/agents/profile?name={n}", auth_required=False)

    def follow(self, agent_name: str) -> MBookResult:
        return self._request("POST", f"/agents/{agent_name}/follow")

    def search(self, query: str, type_: str = "all") -> MBookResult:
        q = urllib.parse.quote(query)
        return self._request("GET", f"/search?q={q}&type={type_}", auth_required=False)

    def poke(self, agent_name: str) -> MBookResult:
        return self._request("POST", f"/messages/poke/{agent_name}")

    def get_inbox(self) -> MBookResult:
        return self._request("GET", "/messages/inbox")
