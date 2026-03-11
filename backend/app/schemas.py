from typing import List, Optional

from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    product_name: Optional[str] = None
    brand_name: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    dimensions: Optional[str] = None
    weight: Optional[str] = None
    key_features: Optional[List[str]] = Field(default_factory=list)
    target_customer: Optional[str] = None
    use_case: Optional[str] = None
    primary_keywords: Optional[List[str]] = Field(default_factory=list)
    secondary_keywords: Optional[List[str]] = Field(default_factory=list)


class VisionAnalysisResult(BaseModel):
    product_type: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    colors: List[str] = Field(default_factory=list)
    design_style: Optional[str] = None
    decorative_features: List[str] = Field(default_factory=list)
    texture: Optional[str] = None
    craftsmanship_style: Optional[str] = None


class ListingOutput(BaseModel):
    title: str
    bullet_points: List[str]
    description: str
    backend_search_terms: str
    image_captions: List[str]


class GenerationResult(BaseModel):
    merged_data: dict
    image_analysis: Optional[VisionAnalysisResult] = None
    keywords: List[str]
    use_cases: List[str]
    listing: ListingOutput
