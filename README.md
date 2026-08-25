# AI Website Summarizer

## Table of contents

- [Project Overview](#project-overview)
- [Goal](#goal)
- [Data Structure](#data-structure)
- [Tools](#tools)
- [How It Works](#how-it-works)
- [Setup & Usage](#setup--usage)
- [Limitations](#limitations)
- [Possible Extensions](#possible-extensions)

## Project Overview

A small Gradio application that takes any public website URL, scrapes its visible text content, and produces a short, friendly markdown summary using an OpenAI chat model. Built as a minimal example of chaining a scraper → LLM → UI pipeline.

## Goal

- Primary Objective: given a URL, return a readable summary of the page content in under a few seconds, without the user having to read the raw page.
- Secondary Objective: demonstrate a clean three-layer separation — data collection (scraper), reasoning (LLM call), and presentation (UI) — each in its own file.

## Data Structure

There is no stored dataset. Input is a single URL string provided by the user at runtime. The scraper fetches the page live and returns:
- Page title
- Cleaned visible text (navigation, scripts, styles, headers, footers, images, and inputs stripped out before summarization)

## Tools

- **Python** — application logic
- **Gradio** — web UI (`gr.Interface`)
- **OpenAI API** (`gpt-4o-mini`) — summarization
- **Requests + BeautifulSoup4** — HTTP fetch and HTML parsing
- **python-dotenv** — environment variable loading

## How It Works

```
scrapper.py   → fetch_website_contents(url): fetches the page, strips noise, returns title + text
summarizer.py → summarize(url): calls scraper, sends result to gpt-4o-mini with a summarization
                system prompt, returns markdown
app.py        → wraps summarize() in a Gradio Interface (textbox in, markdown out)
```

Request flow: **user enters URL → `app.py` → `summarizer.py` → `scrapper.py` (fetch + clean) → back to `summarizer.py` (LLM call) → markdown rendered in UI**.

## Setup & Usage

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your OPENAI_API_KEY
python app.py
```

This launches a local Gradio server (default `http://127.0.0.1:7860`) and, because `share=True` is set, also prints a temporary public link.

## Limitations

- No caching — every request re-scrapes and re-summarizes, even for the same URL.
- No handling of JavaScript-rendered pages (BeautifulSoup only sees static HTML).
- No retry logic beyond the scraper's single request timeout (15s).
- Summaries are not evaluated for accuracy or faithfulness — this is a demo pipeline, not a production summarization service.
- Requires a valid `OPENAI_API_KEY` with available quota; the app gives no fallback if the key is missing or invalid beyond OpenAI's own error message.

## Possible Extensions

- Add response caching keyed by URL.
- Add a headless browser (e.g. Playwright) for JS-heavy sites.
- Add a language-detection step to summarize in the source language.
- Add automated tests for the scraper against a fixed set of sample pages.