import json
import os


class DataManager:

    def __init__(self, json_dir: str = "./summaries"):
        self.json_dir = json_dir

    def list_available_categories(self) -> list[str]:
        if not os.path.exists(self.json_dir):
            return []
        return [
            f
            for f in os.listdir(self.json_dir)
            if not f.startswith(".")
            and os.path.isfile(os.path.join(self.json_dir, f))
        ]

    def get_category_data(self, json_filename: str) -> dict:
        if not json_filename.endswith(".json"):
            json_filename = f"{json_filename}.json"

        filepath = os.path.join(self.json_dir, json_filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{json_filename}' not found.")

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)