# app_cli.py
import os, json, time
from openai import OpenAI
from dotenv import load_dotenv
from prompts import qa_prompt, summarize_prompt, creative_prompt

# load API key from .env
load_dotenv()

# choose model (you can change later if needed)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# create OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_model(prompt_text):
    """Send a prompt to the model and return its response."""
    resp = client.responses.create(
        model=MODEL,
        input=prompt_text
    )
    return (resp.output_text or "").strip()

def log_feedback(entry, path="feedback.json"):
    """Save user feedback to a JSON file."""
    data = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def do_qa():
    q = input("Ask your question: ").strip()
    v = input("Prompt variant (0/1/2; Enter=0): ").strip()
    variant = int(v) if v.isdigit() else 0
    out = call_model(qa_prompt(q, variant))
    print("\nAssistant:\n", out)
    fb = input("\nWas this helpful? (y/n): ").strip().lower().startswith("y")
    log_feedback({"ts": int(time.time()), "task": "qa", "variant": variant,
                  "input": q, "output": out, "helpful": fb})

def do_summarize():
    print("Paste the text to summarize. End with a single line: END")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    text = "\n".join(lines)
    v = input("Prompt variant (0/1/2; Enter=0): ").strip()
    variant = int(v) if v.isdigit() else 0
    out = call_model(summarize_prompt(text, variant))
    print("\nSummary:\n", out)
    fb = input("\nWas this helpful? (y/n): ").strip().lower().startswith("y")
    log_feedback({"ts": int(time.time()), "task": "summarize", "variant": variant,
                  "input_len": len(text), "output": out, "helpful": fb})

def do_creative():
    topic = input("Describe your idea/topic: ").strip()
    v = input("Prompt variant (0/1/2; Enter=0): ").strip()
    variant = int(v) if v.isdigit() else 0
    out = call_model(creative_prompt(topic, variant))
    print("\nCreative Output:\n", out)
    fb = input("\nWas this helpful? (y/n): ").strip().lower().startswith("y")
    log_feedback({"ts": int(time.time()), "task": "creative", "variant": variant,
                  "input": topic, "output": out, "helpful": fb})

def main():
    print("=== AI Assistant (CLI) ===")
    while True:
        print("\n1) Answer Questions")
        print("2) Summarize Text")
        print("3) Generate Creative Content")
        print("4) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            do_qa()
        elif choice == "2":
            do_summarize()
        elif choice == "3":
            do_creative()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try 1-4.")

if __name__ == "__main__":
    main()
