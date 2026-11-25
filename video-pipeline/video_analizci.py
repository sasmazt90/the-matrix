"""
VIDEO_ANALYZER.PY — YouTube Video Analizi (Gemini)
Slayt 41 — Multimodal Ajan Yetenekleri
"""
import json
import google.generativeai as genai

model = genai.GenerativeModel("gemini-1.5-pro")


def analyze_tutorial(youtube_url: str) -> dict:
    response = model.generate_content(
        [
            {"video_url": youtube_url},
            """Bu tutorial videosunu analiz et.
            JSON formatta döndür:
            {
              "baslik": str,
              "adimlar": [{"num": int, "aciklama": str, "kod": str}],
              "gereksinimler": [str],
              "sure_dakika": int
            }""",
        ]
    )
    return json.loads(response.text)


# Sonuç: Tam adım adım rehber, otomatik üretildi
