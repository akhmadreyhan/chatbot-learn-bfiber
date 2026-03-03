from llm import load_llm
import json


llm = load_llm()

route_prompt = """
Klasifikasikan pesan pengguna ke dalam salah satu domain berikut:
- sales order agent
- core network agent
- ont agent
- other network system
Petunjuk:
- sales order agent: pesan pengguna berkaitan dengan bantuan pelanggan, seperti gangguan massal, cek internet, pembayaran tagihan, domisili pengguna, cek paket internet pengguna, status pengguna, riwayat pembayaran terakhir, ONT perangkat.
- core network agent: pesan pengguna berkaitan dengan masalah sinyal, seperti jaringan overload, status layanan, sesi login, dll.
- ont agent: pesan pengguna berkaitan dengan masalah router/modem, seperti ping, restart, matikan, ganti password, tes kecepatan, dll.
- other network system: pesan pengguna berkaitan dengan pertanyaan umum (FAQ), seperti bagaimana cara, apa itu, dll.
Catatan:
- Jika pesan pengguna tidak berkaitan dengan domain mana pun di atas, kembalikan "chitchat"
- Gunakan konteks percakapan sebelumnya untuk memahami pesan lanjutan. Contohnya, jika asisten baru saja menanyakan ID pelanggan dan pengguna merespons dengan angka, klasifikasikan pesan tersebut berdasarkan topik obrolan saat ini.
Kembalikan dalam format JSON murni:
{"domain": "..."}
"""

def detect_route(message: str, context: list = None) -> str:
    prompt = "Instructions: \n" + route_prompt

    if context:
        prompt += "\nRecent conversation:\n"
        for msg in context:
            prompt += f"- {msg['role']}: {msg['content']}\n"

    prompt += "\nUser message:\n" + message

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)
        return data.get("domain", "chitchat")
    except Exception as e:
        return f"Error: {e}"