"""
CHAT_ROOM.PY — ANA DÖNGÜ
Slayt 59 — Sohbet Odası Kurulumu
"""
import asyncio
from anthropic import AsyncAnthropic

from agent_roles import AGENT_ROLES
from moderator_prompt import moderate

client = AsyncAnthropic()


async def call_agent(system: str, messages: list) -> str:
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,  # Kısa, odaklı yanıtlar
        system=system,
        messages=messages,
    )
    return response.content[0].text


async def run_chat_room(question: str) -> str:
    # Paylaşılan bağlamı başlat
    history = [{"role": "user", "content": question}]
    agents = ["savunucu", "elestirel", "analist"]

    for round_num in range(3):  # max 3 tur
        # Her ajan sırayla konuşur
        for agent_id in agents:
            role = AGENT_ROLES.get(agent_id, {})
            response = await call_agent(
                system=role.get("system", ""),
                messages=history,
            )
            history.append({
                "role": "assistant",
                "content": f"[{role.get('name', agent_id)}]: {response}",
            })

        # Moderatör konsensüs kontrolü
        result = await moderate(history)
        if result["status"] == "done":
            return result["decision"]

    return "Tur limiti aşıldı — son durum döndürülüyor"


if __name__ == "__main__":
    print(asyncio.run(run_chat_room(
        "Yeni proje için Microservices mi, Monolith mi?"
    )))
