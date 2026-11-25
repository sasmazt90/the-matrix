"""
ESCALATION_NOTIFIER.PY
Slayt 70 — İnsan Onay Noktaları
"""


async def notify_human(task, error):
    payload = {
        "title": "İnsan Onayı Gerekli",
        "task": task.description,
        "severity": "critical",
        "actions": ["approve", "reject", "retry"],
    }
    await slack.send(payload)
    return await wait_for_decision()


# KARAR AKIŞI
# Doğrulama geçti mi?
#   ↓ EVET → otomatik onay → deploy
#   ↓ HAYIR → Slack/Email bildirimi → bekle


# --- Yer tutucular ---


class _Slack:
    async def send(self, payload):
        ...


slack = _Slack()


async def wait_for_decision():
    return "approve"
