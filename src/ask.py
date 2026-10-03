import sys

from src.generate import answer

question = " ".join(sys.argv[1:])
text, hits = answer(question)

print(text)
print("\nИсточники:")
for i, h in enumerate(hits, start=1):
    print(f"  [{i}] {h['source']} | {h['location']} | {h['score']:.2f}")
