from fastmcp import FastMCP
import random
import sys
import logging
from datetime import datetime, timedelta

# IMPORTANT: never print() in MCP stdio server
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

mcp = FastMCP("Telco Mock MCP")

# =========================
# Helper
# =========================
def _rand_bool(p=0.7):
    return random.random() < p

def _rand_date(days=120):
    d = datetime.now() - timedelta(days=random.randint(0, days))
    return d.strftime("%Y-%m-%d")

def _rand_ip():
    return f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(2,254)}"

def _rand_service_id():
    return f"CN-{random.randint(100000,999999)}"

def _rand_area():
    return random.choice(["Jakarta", "Bandung", "Tangerang", "Bekasi", "Depok"])

def _rand_package():
    return random.choice(["platinum", "gold", "silver"])


# =========================
# ✅ SO MASTER TOOL (DISATUIN)
# =========================
@mcp.tool()
def so_get_profile(id: str) -> dict:
    """
    [MASTER] Ambil profil lengkap pelanggan berdasarkan ID.

    PAKAI INI PERTAMA kalau user:
    - "internet mati", "wifi mati", "lemot", "putus-putus"
    - "cek tagihan", "cek paket", "cek status", "mau restart modem tapi gak tau IP"
    - intinya: user kasih ID -> butuh semua info untuk troubleshooting.

    Parameter:
    - id (str): ID pelanggan. contoh: "12345"

    Output jika BUKAN pelanggan:
    - {
        "customer": "tidak",
        "id": "<id>"
      }

    Output jika pelanggan:
    - {
        "customer": "ya",
        "id": "<id>",
        "daerah": "Jakarta/Bandung/...",
        "paket": "platinum/gold/silver",
        "ip": "10.x.x.x",
        "service_id_cn": "CN-123456",
        "status_pelanggan": "aktif/suspend/berhenti",
        "tanggal_terakhir_bayar": "YYYY-MM-DD",
        "tagihan": {
          "tunggakan_bulan": 1-6,
          "total_tagihan": <rupiah>
        }
      }
    """
    is_customer = _rand_bool(0.85)
    if not is_customer:
        return {"customer": "tidak", "id": id}

    tunggakan = random.randint(0, 6)  # boleh 0 juga biar realistis
    total = 0 if tunggakan == 0 else random.randint(100_000, 5_000_000)

    return {
        "customer": "ya",
        "id": id,
        "daerah": _rand_area(),
        "paket": _rand_package(),
        "ip": _rand_ip(),
        "service_id_cn": _rand_service_id(),
        "status_pelanggan": random.choice(["aktif", "suspend", "berhenti"]),
        "tanggal_terakhir_bayar": _rand_date(180),
        "tagihan": {
            "tunggakan_bulan": tunggakan,
            "total_tagihan": total
        }
    }


# =========================
# API SO Agent (tetap)
# =========================
@mcp.tool()
def ubah_paket_langganan(id: str, paket_sebelumnya: str) -> dict:
    """
    Ubah paket langganan pelanggan.

    Pakai jika user minta upgrade/downgrade paket.
    Biasanya kamu ambil paket_sebelumnya dari so_get_profile(id).

    Parameter:
    - id (str)
    - paket_sebelumnya (str): contoh "gold"

    Output:
    - {"success": true/false, "paket_sekarang": "..."}
    """
    success = _rand_bool()
    return {"success": success, "paket_sekarang": _rand_package() if success else paket_sebelumnya}


@mcp.tool()
def pindah_alamat(id: str) -> dict:
    """
    Pindah alamat pelanggan.

    Parameter:
    - id (str)

    Output:
    - {"success": true/false, "alamat_baru": "..."/null}
    """
    success = _rand_bool()
    return {"success": success, "alamat_baru": f"Jl. Contoh No.{random.randint(1,200)}, {_rand_area()}" if success else None}


@mcp.tool()
def bayar_tagihan(id: str) -> dict:
    """
    Simulasi bayar tagihan.

    Parameter:
    - id (str)

    Output:
    - {"success": true/false, "message":"berhasil/gagal/saldo tidak sesuai"}
    """
    success = _rand_bool()
    message = "berhasil" if success else random.choice(["saldo tidak sesuai", "gagal"])
    return {"success": success, "message": message}


@mcp.tool()
def berhenti_langganan(id: str) -> dict:
    """
    Berhenti langganan.

    Parameter:
    - id (str)

    Output:
    - {"success": true/false, "message":"berhasil/gagal"}
    """
    return {"success": _rand_bool(), "message": random.choice(["berhasil", "gagal"])}


@mcp.tool()
def mau_langganan(nama: str, domisili: str) -> dict:
    """
    Daftar pelanggan baru.

    Parameter:
    - nama (str)
    - domisili (str)

    Output:
    - {"id_baru": "CUST-xxxxxx"}
    """
    return {"id_baru": f"CUST-{random.randint(100000,999999)}"}


@mcp.tool()
def aktifkan_ulang_langganan(id: str) -> dict:
    """
    Aktifkan ulang pelanggan (misal habis berhenti/suspend).

    Parameter:
    - id (str)

    Output:
    - {"success": true/false}
    """
    return {"success": _rand_bool()}


@mcp.tool()
def update_data_pelanggan(id: str, alamat: str = "", no_hp: str = "") -> dict:
    """
    Update data pelanggan.

    Parameter:
    - id (str)
    - alamat (str, optional)
    - no_hp (str, optional)

    Output:
    - {"success": true/false}
    """
    return {"success": _rand_bool()}


# =========================
# Ticket Agent
# =========================
@mcp.tool()
def teknisi_datang_kerumah(id: str, alamat_dituju: str) -> dict:
    """
    Buat tiket kunjungan teknisi ke rumah.

    Parameter:
    - id (str)
    - alamat_dituju (str): alamat tujuan teknisi

    Output:
    - {"ticket_id": "TCK-xxxxx"}
    """
    return {"ticket_id": f"TCK-{random.randint(10000,99999)}"}


@mcp.tool()
def ticket_kecepatan_internet_tidak_sesuai(service_id_cn: str) -> dict:
    """
    Buat tiket: kecepatan internet tidak sesuai.

    Parameter:
    - service_id_cn (str)

    Output:
    - {"ticket_id": "TCK-CN-xxxxx"}
    """
    return {"ticket_id": f"TCK-CN-{random.randint(10000,99999)}"}


@mcp.tool()
def ticket_jaringan_overload(service_id_cn: str) -> dict:
    """
    Buat tiket: jaringan overload.

    Parameter:
    - service_id_cn (str)

    Output:
    - {"ticket_id": "TCK-CN-xxxxx"}
    """
    return {"ticket_id": f"TCK-CN-{random.randint(10000,99999)}"}


if __name__ == "__main__":
    mcp.run()