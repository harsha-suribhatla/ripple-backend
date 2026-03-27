from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic
import requests
from urllib.parse import urlparse, parse_qs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key="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")

@app.post("/extract")
async def extract(data: dict):
    url = data.get("url")

    # Fetch the page title from the URL
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        page_title = ""
        if "<title>" in response.text:
            page_title = response.text.split("<title>")[1].split("</title>")[0]
    except:
        page_title = ""

    # Ask Claude to extract the movie/show title
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