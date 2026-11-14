
from .groq_client import GroqClient


class FertilizerScanner:
    """Identify fertilizer products using Groq AI vision."""

    def __init__(self, api_key=None):
        self.api_key = api_key

    def scan(self, image_path):
        prompt = """
        Analyze the uploaded agricultural fertilizer image.

        Provide the following information:

        1. PRODUCT NAME:
        2. NPK CONTENT:
        3. SAFETY:
        4. SUITABLE CROPS:
        5. RECOMMENDED DOSAGE:
        6. APPLICATION METHOD:

        If any information is not visible on the package,
        clearly mention that it is not identifiable.
        Do not invent product details.
        """

        client = GroqClient(api_key=self.api_key)

        response = client.generate_content(
            prompt=prompt,
            image_path=image_path
        )

        if response:
            return response.strip()

        return "Fertilizer scanner unavailable. Please try again."
