"""
MCP Server — calls api_mockup FastAPI endpoints via HTTP.
Jalankan api_mockup dulu:  uvicorn api_mockup:app --port 8000
"""
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
def validate_customer(nik: str) -> dict:
    """Validasi pelanggan berdasarkan NIK, lalu buka tiket dan mulai SLA."""
    return _post("/so/customer/validate", {"nik": nik})


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Cek status dan detail tiket pelanggan."""
    return _get(f"/so/ticket/{ticket_id}")


@mcp.tool()
def check_gamas(region_code: str, billing_account: Optional[str] = None) -> dict:
    """Cek apakah ada gangguan massal (Gamas) di wilayah pelanggan."""
    body: dict = {"region_code": region_code}
    if billing_account:
        body["billing_account"] = billing_account
    return _post("/gamas/check", body)


@mcp.tool()
def check_billing(billing_account: str) -> dict:
    """Cek tagihan outstanding pelanggan."""
    return _get("/billing/outstanding", billing_account=billing_account)

@mcp.tool()
def create_escalation(
    billing_account: str,
    customer_id: str,
    ticket_id: str,
    issue_type: str = "TOTAL_OUTAGE",
    notes: Optional[str] = None,
) -> dict:
    """Buat tiket eskalasi ke NOC/FTTX jika troubleshooting L1 gagal."""
    body: dict = {
        "billing_account": billing_account,
        "customer_id": customer_id,
        "ticket_id": ticket_id,
        "issue_type": issue_type,
    }
    if notes:
        body["notes"] = notes
    return _post("/noc/ticket", body)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="172.16.7.42", port=8910)