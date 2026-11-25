"""
Slayt 42 — Transkript + kare birleştirme
"""
EXTRACTION_PROMPT = """Bu videodaki adımları, kodu ve gereksinimleri JSON
olarak çıkar. Sadece videoda görülen bilgileri kullan, tahmin etme."""


def analyze_with_frames(transcript: str, frames: list, model) -> str:
    content = [
        {"text": f"Transkript:\n{transcript}"},
    ]
    for frame in frames[::5]:  # Her 5. kare
        content.append({"image": frame})
    content.append({"text": EXTRACTION_PROMPT})
    return model.generate_content(content)
