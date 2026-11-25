"""
COST MONITOR
Slayt 97 — Cost Monitoring & Alerting

Anthropic API çağrılarının token kullanımını ve maliyetini izler.
Eşik değerlerinde Slack ve email bildirimi gönderir.
"""

import os
import json
import sqlite3
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional

import anthropic
import requests


# Pricing per 1M tokens (2026)
PRICING = {
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4-7": {"input": 15.00, "output": 75.00},
    "claude-opus-4-7-1m": {"input": 30.00, "output": 150.00},
}


@dataclass
class CostRecord:
    timestamp: str
    model: str
    task_id: str
    input_tokens: int
    output_tokens: int
    cache_creation_tokens: int
    cache_read_tokens: int
    cost_usd: float


class CostMonitor:
    def __init__(self, db_path: str = "~/.claude/cost.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """CREATE TABLE IF NOT EXISTS cost_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                model TEXT NOT NULL,
                task_id TEXT,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cache_creation_tokens INTEGER,
                cache_read_tokens INTEGER,
                cost_usd REAL
            )"""
        )
        conn.commit()
        conn.close()

    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
    ) -> float:
        prices = PRICING.get(model)
        if not prices:
            return 0.0

        # Standard input
        cost = (input_tokens / 1_000_000) * prices["input"]
        # Output
        cost += (output_tokens / 1_000_000) * prices["output"]
        # Cache writes (25% extra)
        cost += (cache_creation_tokens / 1_000_000) * prices["input"] * 1.25
        # Cache reads (90% discount)
        cost += (cache_read_tokens / 1_000_000) * prices["input"] * 0.10

        return round(cost, 6)

    def log(self, record: CostRecord):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT INTO cost_records
               (timestamp, model, task_id, input_tokens, output_tokens,
                cache_creation_tokens, cache_read_tokens, cost_usd)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record.timestamp,
                record.model,
                record.task_id,
                record.input_tokens,
                record.output_tokens,
                record.cache_creation_tokens,
                record.cache_read_tokens,
                record.cost_usd,
            ),
        )
        conn.commit()
        conn.close()

    def daily_cost(self, date: Optional[str] = None) -> dict:
        date = date or datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute(
            """SELECT
                SUM(cost_usd) as total,
                COUNT(*) as requests,
                SUM(input_tokens) as input,
                SUM(output_tokens) as output,
                SUM(cache_read_tokens) as cache_read
               FROM cost_records
               WHERE timestamp LIKE ? || '%'""",
            (date,),
        )
        row = cur.fetchone()
        conn.close()
        return {
            "date": date,
            "total_usd": round(row[0] or 0, 4),
            "requests": row[1] or 0,
            "input_tokens": row[2] or 0,
            "output_tokens": row[3] or 0,
            "cache_read_tokens": row[4] or 0,
            "cache_hit_rate": (
                round((row[4] or 0) / max(1, (row[2] or 0) + (row[4] or 0)) * 100, 1)
            ),
        }

    def check_thresholds(self) -> list:
        """Bütçe uyarı eşiklerini kontrol et, ihlal varsa liste döndür."""
        today = self.daily_cost()
        alerts = []

        thresholds = [
            (50, "warning", "email"),
            (100, "critical", "slack"),
            (200, "halt", "slack+email"),
        ]
        for threshold, severity, channel in thresholds:
            if today["total_usd"] >= threshold:
                alerts.append(
                    {
                        "severity": severity,
                        "channel": channel,
                        "threshold": threshold,
                        "actual": today["total_usd"],
                        "date": today["date"],
                    }
                )
        return alerts

    async def send_alert(self, alert: dict):
        message = (
            f"🚨 Anthropic API maliyet uyarısı\n"
            f"Bugünkü toplam: ${alert['actual']}\n"
            f"Eşik: ${alert['threshold']}\n"
            f"Severity: {alert['severity']}"
        )
        if "slack" in alert["channel"] and (url := os.environ.get("SLACK_WEBHOOK_URL")):
            requests.post(url, json={"text": message}, timeout=5)
        if "email" in alert["channel"]:
            # Email gönderme implementasyonu (örn: Resend, SES)
            print(f"[email] {message}")


# ----------------------------------------------------------------------------
# Cost-aware client wrapper
# ----------------------------------------------------------------------------
class TrackedAnthropic:
    """Anthropic client wrapper'ı, her çağrıyı CostMonitor'a loglar."""

    def __init__(self, monitor: CostMonitor):
        self.client = anthropic.Anthropic()
        self.monitor = monitor

    def messages_create(self, **kwargs):
        task_id = kwargs.pop("task_id", "untracked")
        response = self.client.messages.create(**kwargs)

        usage = response.usage
        cost = self.monitor.calculate_cost(
            model=kwargs["model"],
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_creation_tokens=getattr(usage, "cache_creation_input_tokens", 0),
            cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0),
        )

        self.monitor.log(
            CostRecord(
                timestamp=datetime.utcnow().isoformat(),
                model=kwargs["model"],
                task_id=task_id,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_creation_tokens=getattr(usage, "cache_creation_input_tokens", 0),
                cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0),
                cost_usd=cost,
            )
        )

        return response


# ----------------------------------------------------------------------------
# CLI: günlük rapor
# ----------------------------------------------------------------------------
async def main():
    monitor = CostMonitor()
    today = monitor.daily_cost()

    print(f"\n📊 Anthropic API Kullanımı — {today['date']}\n")
    print(f"  Toplam:     ${today['total_usd']}")
    print(f"  İstekler:   {today['requests']}")
    print(f"  Input:      {today['input_tokens']:,} tokens")
    print(f"  Output:     {today['output_tokens']:,} tokens")
    print(f"  Cache hit:  %{today['cache_hit_rate']}")

    alerts = monitor.check_thresholds()
    if alerts:
        print("\n🚨 Uyarılar:")
        for alert in alerts:
            print(f"  - {alert['severity']}: ${alert['actual']} >= ${alert['threshold']}")
            await monitor.send_alert(alert)
    else:
        print("\n✓ Bütçe içinde")


if __name__ == "__main__":
    asyncio.run(main())
