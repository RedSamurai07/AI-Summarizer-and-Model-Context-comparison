{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9199d414",
   "metadata": {},
   "outputs": [],
   "source": [
    "from openai import OpenAI\n",
    "from dotenv import load_dotenv\n",
    "from scraper import fetch_website_contents\n",
    "\n",
    "load_dotenv()\n",
    "client = OpenAI()\n",
    "\n",
    "system_prompt = \"\"\"You analyze the contents of a website and\n",
    "give a short, friendly summary. Ignore navigation menus.\n",
    "Respond in markdown.\"\"\"\n",
    "\n",
    "def summarize(url):\n",
    "    website = fetch_website_contents(url)\n",
    "    response = client.chat.completions.create(\n",
    "        model=\"gpt-4o-mini\",\n",
    "        messages=[\n",
    "            {\"role\": \"system\", \"content\": system_prompt},\n",
    "            {\"role\": \"user\",   \"content\": f\"Summarize this website:\\n\\n{website}\"},\n",
    "        ],\n",
    "    )\n",
    "    return response.choices[0].message.content"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "py310 (3.10.20)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.20"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
