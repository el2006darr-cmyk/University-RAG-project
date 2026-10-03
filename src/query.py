import sys

from src.store import search

question = " ".join(sys.argv[1:])
for hit in search(question):
    print(f"{hit['score']:.2f} | {hit['source']} | {hit['location']}")
    print("   ", hit["text"][:150].replace("\n", " / "))
