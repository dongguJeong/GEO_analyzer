import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from typing import Literal


load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

claude_client = Anthropic(
    api_key=os.getenv("CLAUDE_API_KEY")
)


SYSTEM_PROMPT = """
당신은 GEO 전문가입니다.

다음 항목을 0~10점으로 평가하세요.

- readability
- expertise
- trustworthiness
- faq
- summary

JSON만 출력하세요.

{
  "readability":0,
  "expertise":0,
  "trustworthiness":0,
  "faq":0,
  "summary":0,
  "strengths":[],
  "weaknesses":[],
  "suggestions":[]
}
"""

def analyze(content: str, llm: Literal["openai", "claude"]):

    if llm.lower() == "claude":
        response = claude_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        text = response.content[0].text
        text = text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(text)

    else:
        response = openai_client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return json.loads(response.output_text)