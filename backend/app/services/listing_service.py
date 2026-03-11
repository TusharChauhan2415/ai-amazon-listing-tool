from typing import Any, Dict, List

from app.schemas import ProductInput
from app.services.openai_service import OpenAIService


class ListingService:
    def __init__(self) -> None:
        self.ai = OpenAIService()

    @staticmethod
    def _merge_data(user_data: Dict[str, Any], image_data: Dict[str, Any]) -> Dict[str, Any]:
        merged = dict(user_data)

        def fill(field: str, image_field: str | None = None):
            source_field = image_field or field
            if not merged.get(field) and image_data.get(source_field):
                value = image_data[source_field]
                if isinstance(value, list):
                    merged[field] = ", ".join(value)
                else:
                    merged[field] = value

        fill("category")
        fill("material")
        fill("color", "colors")

        if not merged.get("product_name") and image_data.get("product_type"):
            merged["product_name"] = image_data["product_type"]

        if not merged.get("key_features"):
            merged["key_features"] = image_data.get("decorative_features", [])

        return merged

    async def generate(self, user_input: ProductInput, images: List[bytes]) -> Dict[str, Any]:
        image_analysis = self.ai.analyze_images(images) if images else None
        user_data = user_input.model_dump()
        merged_data = self._merge_data(user_data, image_analysis or {})

        keywords = self.ai.generate_keywords(merged_data)
        use_cases = self.ai.generate_use_cases(merged_data)
        listing = self.ai.generate_listing({**merged_data, "keywords": keywords, "use_cases": use_cases})

        return {
            "merged_data": merged_data,
            "image_analysis": image_analysis,
            "keywords": keywords,
            "use_cases": use_cases,
            "listing": listing,
        }
