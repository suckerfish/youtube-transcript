from openai import OpenAI
import os


class Perplex:
    def __init__(self):
        self.api_key = os.getenv("perplexity_key")
        self.baseurl = "https://api.perplexity.ai"
        self.model = "llama-3-70b-instruct"
        self.client = OpenAI(api_key=self.api_key, base_url=self.baseurl)

    def ask(self, prompt):
        messages = [
            {"role": "system",
             "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
            {"role": "user", "content": f"{prompt}"},
        ]
        response = self.client.chat.completions.create(model=self.model, messages=messages)
        print(response.choices[0].message.content)

