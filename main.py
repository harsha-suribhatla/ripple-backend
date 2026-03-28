from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.post("/extract")
async def extract(data: dict):
    url = data.get("url")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        page_title = ""
        if "<title>" in response.text:
            page_title = response.text.split("<title>")[1].split("</title>")[0]
    except:
        page_title = ""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"URL: {url}\nPage title: {page_title}\n\nWhat movie or TV show is this about? Reply with ONLY the title, nothing else. If you cannot tell, reply with UNKNOWN."
            }
        ]
    )

    title = message.content[0].text.strip()
    return {"title": title}

@app.get("/")
def root():
    return {"status": "Ripple backend is running"}