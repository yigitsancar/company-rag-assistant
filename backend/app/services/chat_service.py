from openai import OpenAI

from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def ask_openai(question: str, context: str) -> str:
    prompt = f"""
Sen Company RAG Assistant adlı kurumsal belge asistanısın.

Kurallar:
- Sadece verilen belge içeriğine göre cevap ver.
- Belge içeriğinde cevap yoksa "Bu bilgi yüklenen belgede bulunamadı." de.
- Cevabı kısa, net ve Türkçe ver.

Belge içeriği:
{context}

Soru:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
