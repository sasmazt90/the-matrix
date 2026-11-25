"""
PYTHON'DA KULLANIM
Slayt 16 — API Güvenliği
"""
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ["OPENAI_API_KEY"]
print(f"API anahtarı yüklendi: {key[:8]}...")
