from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    tone: Mapped[str] = mapped_column(String(50))
    length: Mapped[str] = mapped_column(String(20))
    keywords: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text)
    seo_score: Mapped[Optional[float]] = mapped_column(Float)
    word_count: Mapped[Optional[int]] = mapped_column()

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), server_default=func.now())

    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, topic='{self.topic[:30]}...')>"
