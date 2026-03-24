from groq import Groq
from app import config

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        
    def generate(self, prompt):
        res = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=config.GROQ_MODEL,
            temperature=0.2
        )
        return res.choices[0].message.content
