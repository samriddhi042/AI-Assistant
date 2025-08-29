# prompts.py
# This file holds reusable prompt templates for the assistant.

# Q&A (3 styles)
QA_SYSTEM = [
    "You are a concise factual assistant. Cite key facts briefly when relevant.",
    "You are a friendly tutor. Explain simply with 2–3 short sentences.",
    "You are a strict fact-checker. Answer only if confident; otherwise say you’re unsure."
]

def qa_prompt(user_q, variant=0):
    system = QA_SYSTEM[variant % len(QA_SYSTEM)]
    return f"{system}\n\nQuestion: {user_q}\nAnswer:"

# Summarization (3 styles)
SUMM_STYLES = [
    "Summarize in 3 sentences, keep key numbers/names.",
    "Summarize as 5 bullet points (no fluff).",
    "Summarize for a 12-year-old, simple words, 3–5 lines."
]

def summarize_prompt(text, variant=0):
    style = SUMM_STYLES[variant % len(SUMM_STYLES)]
    return f"{style}\n\nTEXT:\n{text}\n\nSummary:"

# Creative writing (3 styles)
CREATIVE_STYLES = [
    "Write a 180–220 word short story; strong imagery; clear arc.",
    "Write a 10–12 line rhyming poem; consistent meter.",
    "Write a 200–250 word reflective essay; 1 twist in the final line."
]

def creative_prompt(topic, variant=0):
    style = CREATIVE_STYLES[variant % len(CREATIVE_STYLES)]
    return f"{style}\n\nTopic: {topic}\n\nOutput:"
