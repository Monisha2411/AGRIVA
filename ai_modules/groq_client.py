
import os
import time
import base64
import mimetypes
import requests
from flask import current_app


class GroqClient:
    """Groq API client for text and image analysis."""

    _session = None

    def __init__(self, api_key=None, model=None):
        try:
            self.api_key = api_key or current_app.config.get("GROQ_API_KEY")
            self.model = model or current_app.config.get(
                "GROQ_MODEL", "llama-3.3-70b-versatile"
            )
        except RuntimeError:
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            self.model = model or os.getenv(
                "GROQ_MODEL", "llama-3.3-70b-versatile"
            )

        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

        if GroqClient._session is None:
            GroqClient._session = requests.Session()

    def generate_content(
        self,
        prompt,
        system_instruction=None,
        temperature=0.7,
        image_path=None
    ):
        if not self.api_key:
            return "Groq API key is missing. Check your .env file."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []

        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })

        if image_path:
            try:
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(
                        image_file.read()
                    ).decode("utf-8")

                mime_type, _ = mimetypes.guess_type(image_path)

                if not mime_type or not mime_type.startswith("image/"):
                    mime_type = "image/jpeg"

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}"
                            }
                        }
                    ]
                })

                current_model = "qwen/qwen3.8-27b"

            except Exception as error:
                print(f"[Groq Image Error] {error}")
                return "Unable to read the uploaded image."

        else:
            messages.append({
                "role": "user",
                "content": prompt
            })
            current_model = self.model

        start_time = time.time()

        try:
            payload = {
                "model": current_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1024
            }

            response = self._session.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]

                print(
                    f"[Groq] {current_model} responded in "
                    f"{time.time() - start_time:.2f}s"
                )

                return answer

            print(
                f"[Groq Error] {response.status_code}: "
                f"{response.text}"
            )

            return f"AI Error: Groq returned {response.status_code}. Check terminal."

        except requests.RequestException as error:
            print(f"[Groq Connection Error] {error}")
            return "Groq AI is unreachable. Check your internet connection."

        except Exception as error:
            print(f"[Groq Error] {error}")
            return "Unable to analyze the request. Please try again."
