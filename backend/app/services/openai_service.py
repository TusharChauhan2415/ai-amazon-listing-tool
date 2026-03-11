import base64
import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from app.prompts.templates import KEYWORD_PROMPT, LISTING_PROMPT, USE_CASE_PROMPT, VISION_PROMPT


class OpenAIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    @staticmethod
    def _safe_json_parse(text: str, default: Any) -> Any:
        try:
            return json.loads(text)
        except Exception:
            return default

    def _chat_json(self, prompt: str, payload: Dict[str, Any], default: Any) -> Any:
        if not self.client:
            return default

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(payload)},
            ],
            text={"format": {"type": "json_object"}},
        )
        raw = response.output_text
        parsed = self._safe_json_parse(raw, default)
        return parsed

    def analyze_images(self, images: List[bytes]) -> Dict[str, Any]:
        default = {
            "product_type": "",
            "category": "",
            "material": "",
            "colors": [],
            "design_style": "",
            "decorative_features": [],
            "texture": "",
            "craftsmanship_style": "",
        }
        if not images:
            return default
        if not self.client:
            return default

        image_content = []
        for blob in images:
            b64 = base64.b64encode(blob).decode("utf-8")
            image_content.append(
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{b64}",
                }
            )

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": VISION_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Analyze these product images."},
                        *image_content,
                    ],
                },
            ],
            text={"format": {"type": "json_object"}},
        )
        return self._safe_json_parse(response.output_text, default)

    def generate_keywords(self, merged_data: Dict[str, Any]) -> List[str]:
        default = [
            "amazon india",
            "home decor",
            "gift item",
            "diwali decor",
            "housewarming gift",
        ]
        data = self._chat_json(KEYWORD_PROMPT, merged_data, {"keywords": default})
        return data.get("keywords", default)[:30]

    def generate_use_cases(self, merged_data: Dict[str, Any]) -> List[str]:
        default = [
            "Home decoration",
            "Pooja room decoration",
            "Diwali decoration",
            "Housewarming gift",
            "Wedding decor",
            "Office decor",
        ]
        data = self._chat_json(USE_CASE_PROMPT, merged_data, {"use_cases": default})
        return data.get("use_cases", default)

    def generate_listing(self, merged_data: Dict[str, Any]) -> Dict[str, Any]:
        default = {
            "title": "Premium Product for Everyday Use | Amazon India",
            "bullet_points": [
                "Quality Material -> Built for durability -> Long-lasting value for daily usage.",
                "Thoughtful Design -> Enhances aesthetics -> Complements modern Indian homes.",
                "Versatile Utility -> Works in multiple scenarios -> Ideal for home, office, and gifting.",
                "Customer-Focused Build -> Easy to use and maintain -> Saves time and effort.",
                "Festival Ready -> Perfect for special occasions -> Great gifting choice across seasons.",
            ],
            "description": "Crafted for Indian households, this product blends practical utility with stylish appeal. It is suitable for everyday use and special occasions, making it a smart choice for personal use or gifting. The quality-focused construction supports durability, while the thoughtful design ensures it fits beautifully in modern and traditional settings. Whether you are upgrading your home setup, decorating for festivals, or selecting a meaningful gift, this product delivers both function and charm. Its versatile nature helps you use it across spaces such as living room, pooja area, office, or event decor. With customer convenience in mind, it offers easy handling and reliable performance. Choose this product to add value, elegance, and utility to your lifestyle.",
            "backend_search_terms": "home decor india gift item festival decor modern design premium quality",
            "image_captions": [
                "Elegant product display for Indian homes",
                "Close-up on premium detailing",
                "Perfect for festive decor styling",
                "Versatile use across spaces",
                "Gift-ready look for special occasions",
            ],
        }
        data = self._chat_json(LISTING_PROMPT, merged_data, default)
        return {
            "title": data.get("title", default["title"]),
            "bullet_points": data.get("bullet_points", default["bullet_points"]),
            "description": data.get("description", default["description"]),
            "backend_search_terms": data.get("backend_search_terms", default["backend_search_terms"]),
            "image_captions": data.get("image_captions", default["image_captions"]),
        }
