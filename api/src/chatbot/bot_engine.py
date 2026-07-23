import os
from openai import OpenAI
from data_loader import DataManager


class PersonaChatbot:

    def __init__(self, summaries_dir: str = "./summaries"):
        self.data_manager = DataManager(json_dir=summaries_dir)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_response(
        self,
        user_message: str,
        category_file: str,
        mode: str = "recommender",
        history: list = None,
    ) -> str:
        category_data = self.data_manager.get_category_data(category_file)
        summary_text = category_data.get("article", "")
        category_name = category_data.get("stats", {}).get(
            "category", "Category"
        )

        if mode == "anti_recommender":
            system_prompt = f"You are a sarcastic anti-shopping assistant for {category_name}. Talk the user out of buying based on this context:\n{summary_text}"
        else:
            system_prompt = f"You are a helpful shopping assistant for {category_name}. Recommend products based on this context:\n{summary_text}"

        messages = [{"role": "system", "content": system_prompt}]

        # Verlauf einfügen, falls vorhanden
        if history:
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        return response.choices[0].message.content
    
    