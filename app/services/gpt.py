from app.config.settings import get_settings
import openai


class GPTService:
    def __init__(self):
        self.settings = get_settings
        openai.api_key = self.settings.openai_api_key

    async def analyze(self, text: str) -> str:
        prompt = f"""
        You are a financial analyst. Classify this Trump post as:
        - "Good for the stock market"
        - "Bad for the stock market"
        - "Not related to the stock market"

        Post: "{text}"
        
        Respond with only one of the three.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
