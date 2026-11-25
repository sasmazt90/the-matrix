"""
Slayt 22 — Kendini Güncelleyen Promptlar
Görev tamamlandıktan sonra çalışır
"""


def update_learnings(task_result):
    # Başarısız mıydı? Ders çıkar
    if task_result.had_errors:
        lesson = analyze_failure(task_result)
        append_to_claude_md(
            f"## Öğrenilen Ders\n{lesson}"
        )

    # Yeni mimari karar keşfedildi mi?
    if task_result.new_pattern:
        append_to_claude_md(
            f"## Mimari Kural\n{task_result.pattern}"
        )

    # Sonraki ajan bu bilgiyle başlar
    return "CLAUDE.md güncellendi"


# ⚠ Risk: Kötü bir ders CLAUDE.md'ye girerse tüm sonraki oturumları etkiler.
# Her otomatik güncellemeyi insan gözden geçirmesi ile onaylayın.


def analyze_failure(task_result):
    """Yer tutucu — gerçek implementasyon projeye bağlıdır."""
    return f"Hata: {task_result.error_summary}"


def append_to_claude_md(text: str) -> None:
    with open("CLAUDE.md", "a", encoding="utf-8") as f:
        f.write("\n" + text + "\n")
