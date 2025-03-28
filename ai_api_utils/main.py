
import os
import json
from openai import OpenAI
from google import genai
from google.genai import types
import logging
import hmac
import os
import subprocess
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    gemini_models=gemini_client.models.list()
except KeyError as e:
 print("no gemini api key found")
 gemini_client=None
 GEMINI_API_KEY = None
try:
    deepseek_api_key = os.environ["DEEPSEEK_API_KEY"]
    deep_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com") 
except KeyError as e:
 print("no deepseek api key found")
 deepseek_api_key = None
 deep_client=None

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "256"))


def generate_gemini_text(prompt, instructions,max_tokens=MAX_TOKENS):
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt,
        config=types.GenerateContentConfig(
        system_instruction=instructions,
        max_output_tokens=max_tokens,
        temperature=0.3,
    ),
    )
    return response.text

def generate_deepseek_text(prompt):
    response = deep_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        stream=False,
        max_tokens=MAX_TOKENS
    )
    return response.choices[0].message.content
