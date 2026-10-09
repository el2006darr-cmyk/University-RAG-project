from src.generate import answer

print("Задавайте вопросы. Пустая строка - выход.")
while True:
    question = input("\n> ").strip()
    if not question:
        break
    text, hits = answer(question)
    print(text)
    print("\nИсточники:")
    for i, h in enumerate(hits, start=1):
        print(f"  [{i}] {h['source']} | {h['location']} | {h['score']:.2f}")
