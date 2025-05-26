from openai import OpenAI

class OpenAIService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, text, sentiment):
        prompt = f"""
You are an AI assistant responding to user feedback.
The sentiment of the feedback is "{sentiment}".

Here is the feedback:
"{text}"

Write a short, empathetic, and context-aware response.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant responding to user feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            print("OpenAI API error:", e)
            return "Sorry, we couldn't generate a response at this time."
