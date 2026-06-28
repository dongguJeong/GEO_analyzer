import json
import os

from dotenv import load_dotenv
from openai import OpenAI

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


openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class OpenAiLLM(BaseLLM) :
    
    def analyze(self, content):

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