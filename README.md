# Ripple Backend 🎬

The FastAPI backend that powers Ripple's AI URL extraction feature.

---

## What It Does

When a user pastes a URL into Ripple, this backend:

1. Fetches the page and extracts the title tag
2. Sends it to Claude (Anthropic) with a prompt to identify the movie or show name
3. Returns the clean title back to the frontend for TMDB lookup

This means users can paste a TikTok link, a YouTube video, or any article and Ripple automatically figures out what show or movie it's about.

---

## Endpoints

### POST /extract

Accepts a URL and returns the extracted title.

**Request**
```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

**Response**
```json
{
  "title": "Inception"
}
```

Returns `"UNKNOWN"` if no title can be extracted.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Python FastAPI |
| AI | Claude API (Anthropic) |
| HTTP | requests, uvicorn |
| Config | python-dotenv |

---

## Running Locally
```bash
git clone https://github.com/harsha-suribhatla/ripple-backend.git
cd ripple-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_anthropic_key
```

Start the server:
```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`

---

## How Claude Is Used

The backend sends a simple prompt to Claude with the page title and asks it to extract just the movie or show name. Claude handles the messy real world cases like titles that include channel names, episode numbers, or reaction video prefixes.

Example input to Claude:
```
"MrBeast Reacts to Inception (2010) Full Movie Review"
```

Claude returns:
```
Inception
```

---

## Part of Ripple

This backend is one piece of the Ripple project. See the main repo for the full frontend and product context.

[github.com/harsha-suribhatla/Ripple](https://github.com/harsha-suribhatla/Ripple)
