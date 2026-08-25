# pip install openai gradio python-dotenv

import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()  # uses OPENAI_API_KEY
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def ask(client, model, prompt):
    r = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content


def battle(prompt):
    a = ask(openai_client, "gpt-4o-mini", prompt)
    b = ask(groq_client, "llama-3.3-70b-versatile", prompt)
    return a, b


def vote(tally, model_key, direction):
    """tally is a per-browser-session dict via gr.State — not a global,
    so concurrent users on a shared link don't stomp on each other's counts."""
    tally[model_key][direction] += 1
    counts_a = tally["a"]
    counts_b = tally["b"]
    label = f"{'Model A' if model_key == 'a' else 'Model B'}"
    verdict_text = f"🗳️ You voted {'👍' if direction == 'up' else '👎'} on {label}"
    counts_text = (
        f"**Model A** — 👍 {counts_a['up']}  ·  👎 {counts_a['down']}"
        f"&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
        f"**Model B** — 👍 {counts_b['up']}  ·  👎 {counts_b['down']}"
    )
    return tally, verdict_text, counts_text


with gr.Blocks(title="LLM Arena") as demo:
    gr.Markdown("# 🥊 LLM Arena — one prompt, two models")

    # one counter dict per browser session, not shared across users
    vote_state = gr.State({"a": {"up": 0, "down": 0}, "b": {"up": 0, "down": 0}})

    prompt = gr.Textbox(label="Ask both models the same thing")
    go = gr.Button("⚔️ Battle!", variant="primary")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🤖 Model A")
            out_a = gr.Markdown()
            with gr.Row():
                up_a = gr.Button("👍")
                down_a = gr.Button("👎")
        with gr.Column():
            gr.Markdown("### 🤖 Model B")
            out_b = gr.Markdown()
            with gr.Row():
                up_b = gr.Button("👍")
                down_b = gr.Button("👎")

    verdict = gr.Markdown()
    scoreboard = gr.Markdown("**Model A** — 👍 0  ·  👎 0   |   **Model B** — 👍 0  ·  👎 0")

    go.click(battle, inputs=prompt, outputs=[out_a, out_b])

    up_a.click(lambda t: vote(t, "a", "up"), inputs=vote_state, outputs=[vote_state, verdict, scoreboard])
    down_a.click(lambda t: vote(t, "a", "down"), inputs=vote_state, outputs=[vote_state, verdict, scoreboard])
    up_b.click(lambda t: vote(t, "b", "up"), inputs=vote_state, outputs=[vote_state, verdict, scoreboard])
    down_b.click(lambda t: vote(t, "b", "down"), inputs=vote_state, outputs=[vote_state, verdict, scoreboard])

demo.launch(share=True)  # → local + public link 🎉