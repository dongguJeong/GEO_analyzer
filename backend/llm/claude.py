import json
import os

from dotenv import load_dotenv
from anthropic import Anthropic

from llm.base import BaseLLM

load_dotenv()

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


claude_client = Anthropic(
    api_key=os.getenv("CLAUDE_API_KEY")
)

class ClaudeLLM(BaseLLM) :
    
    def analyze(self, content):

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