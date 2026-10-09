import os

from dotenv import load_dotenv
from openai import OpenAI

from src.store import search

load_dotenv()

SYSTEM_PROMPT = """Ты помощник, который отвечает на вопросы строго по предоставленным фрагментам документов.
Правила:
- Используй только информацию из фрагментов.
- Если в фрагментах нет ответа и они не относятся к теме вопроса, ответь: "В документах нет информации по этому вопросу."
- Если вопрос сформулирован неточно, но во фрагментах есть близкая информация, приведи её и скажи, чем она отличается от вопроса.
- Отвечай на языке вопроса.
- После утверждений указывай источник в виде [1], [2] по номеру фрагмента."""


def get_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ.get("LLM_BASE_URL") or None,
    )


def answer(question: str, k: int = 4) -> tuple[str, list[dict]]:
    hits = search(question, k=k)
    context = "\n\n".join(
        f"[{i}] ({h['source']}, {h['location']})\n{h['text']}"
        for i, h in enumerate(hits, start=1)
    )
    response = get_client().chat.completions.create(
        model=os.environ["LLM_MODEL"],
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Фрагменты:\n\n{context}\n\nВопрос: {question}"},
        ],
    )
    return response.choices[0].message.content, hits
