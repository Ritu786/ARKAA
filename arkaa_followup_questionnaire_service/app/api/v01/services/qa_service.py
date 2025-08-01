from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
import os
from core.logging_config import set_logger

qa_logger = set_logger(__name__)

# Defining the OpenAI client
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=10))
async def create_qa(prompt: str) -> str:
    try:
        qa_logger.info('Calling OpenAI for QA Genration.')

        response = await client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()
        qa_logger.info(f' QA Response length: {len(answer)} characters.')
        return answer
    except Exception as e:
        qa_logger.error(f"Failed to generate QA response: {e}", exc_info=True)
        return ""
