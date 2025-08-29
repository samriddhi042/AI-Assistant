import os
import json
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from openai import OpenAI
from prompts import qa_prompt, summarize_prompt, creative_prompt

# Load environment variables
load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=API_KEY)

app = Flask(__name__)
app.secret_key = "supersecret"  # Required for flashing messages


def call_model(prompt_text):
    """Call OpenAI and return output text"""
    try:
        resp = client.responses.create(model=MODEL, input=prompt_text)
        return resp.output_text.strip()
    except Exception as e:
        return f"[Error] {e}"


def log_feedback(entry, path="feedback.json"):
    """Save feedback to JSON file"""
    data = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
    data.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    input_text = ""
    mode = "qa"
    variant = 0

    if request.method == "POST":
        mode = request.form.get("mode", "qa")
        variant = int(request.form.get("variant", 0))
        input_text = request.form.get("input_text", "").strip()

        # Pick prompt type
        if mode == "qa":
            prompt = qa_prompt(input_text, variant)
        elif mode == "summarize":
            prompt = summarize_prompt(input_text, variant)
        else:
            prompt = creative_prompt(input_text, variant)

        output = call_model(prompt)

    return render_template("index.html",
                           output=output,
                           input_text=input_text,
                           mode=mode,
                           variant=variant)


@app.route("/feedback", methods=["POST"])
def feedback():
    mode = request.form.get("mode")
    variant = int(request.form.get("variant", 0))
    input_text = request.form.get("input_text", "")
    output_text = request.form.get("output_text", "")
    helpful = request.form.get("helpful") == "yes"

    entry = {
        "ts": int(time.time()),
        "task": mode,
        "variant": variant,
        "input": input_text,
        "output": output_text,
        "helpful": helpful
    }
    log_feedback(entry)
    flash("✅ Feedback saved!", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
