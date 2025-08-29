import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

key = os.environ.get("OPENAI_API_KEY")

if key:
    # only show first and last few characters (keep it safe)
    print("✅ API key loaded successfully:", key[:5] + "..." + key[-5:])
else:
    print("❌ API key not found. Check your .env file.")
