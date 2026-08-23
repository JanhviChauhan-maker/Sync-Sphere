import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("SYNCSPHERE_LLM_API_KEY")
if not key:
    key = os.getenv("OPENROUTER_API_KEY")

r = requests.get("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {key}"})
print("auth/key payload:")
print(json.dumps(r.json(), indent=2))
