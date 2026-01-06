from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

class BlogGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=500, description="Blog topic")
    tone: str = Field(default="Professional", description="Writing tone")
    length: str = Field(default="Medium", description="Blog length")
    keywords: Optional[str] = Field(default=None, description="Comma-separated keywords")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "The Future of Artificial Intelligence",
                "tone": "Professional",
                "length": "Medium",
                "keywords": "AI, Machine Learning, Automation"
            }
        }
    )

class BlogResponse(BaseModel):
    id: int
    topic: str
    tone: str
    length: str
    keywords: Optional[str]
    title: Optional[str]
    content: str
    seo_score: Optional[float]
    word_count: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BlogListResponse(BaseModel):
    total: int
    blogs: List[BlogResponse]

class MessageResponse(BaseModel):
    message: str
    