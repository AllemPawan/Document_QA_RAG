"""Run: python main.py            -> ingest ./docs and run the demo questions
       python main.py "question"  -> ask a single question"""
import sys

from rag_qa import RAGSystem

QUESTIONS = [
    "What are the main ethical concerns in AI deployment?",
    "How can bias enter a machine learning model?",
    "Why are fairness definitions hard to satisfy at the same time?",
    "What privacy risks do large language models pose?",
    "What does the GDPR give individuals with respect to automated decisions?",
    "Why is human oversight sometimes ineffective?",
    "How can misinformation from generative AI be addressed?",
    "How does the EU AI Act regulate AI systems?",
    "What are the core functions of the NIST AI Risk Management Framework?",
    "What are the concrete research problems for AI safety, such as reward hacking?",
    "Which ethical principles appear most often across global AI guidelines?",
    "What kinds of bias are described in machine learning systems?",
    "What is the capital of France?",
]


def show(r: dict) -> None:
    print(f"\nQ: {r['question']}\nA: {r['answer']}\nSources: {', '.join(r['sources'])}")


if __name__ == "__main__":
    rag = RAGSystem()
    print(f"Ingested {rag.ingest('docs')} chunks; store holds {rag.store.count()}.")
    for q in sys.argv[1:] or QUESTIONS:
        show(rag.ask(q))

