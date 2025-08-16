from google import genai


class GeminiLLM:
    def __init__(self):
        super().__init__()
        self.model_name = "gemini-2.5-flash-lite"
        self.client = genai.Client()

    def generate_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text