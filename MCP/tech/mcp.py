import logging
import os
from typing import Optional

import httpx
from fastmcp import FastMCP

logging.getLogger("mcp").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

BASE_URL = os.getenv("API_BASE_URL", "http://172.16.7.42:8910")
mcp = FastMCP("balifiber")

def _get(path: str, **params) -> dict:
    r = httpx.get(f"{BASE_URL}{path}", params=params)
    r.raise_for_status()
    return r.json()


def _post(path: str, body: dict) -> dict:
    r = httpx.post(f"{BASE_URL}{path}", json=body)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def check_ont(ont_serial: str, billing_account: Optional[str] = None) -> dict:
    """Cek status perangkat ONT pelanggan (online, sinyal, alarm)."""
    body: dict = {"ont_serial": ont_serial, "ont_type": "ONT_4_PORT"}
    if billing_account:
        body["billing_account"] = billing_account
    return _post("/cn/ont/check", body)


@mcp.tool()
def restart_ont(ont_serial: str, reason: Optional[str] = None) -> dict:
    """Kirim perintah restart ONT pelanggan."""
    body: dict = {"ont_serial": ont_serial}
    if reason:
        body["reason"] = reason
    return _post("/cn/ont/restart", body)