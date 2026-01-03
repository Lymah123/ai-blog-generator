from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.blog import BlogPost
from app.schemas.blog import (
    BlogGenerateRequest,
    BlogResponse,
    BlogListResponse,
    MessageResponse
)
from app.services.ai_service import hf_service

router = APIRouter()

@router.post("/generate", response_model=BlogResponse, status_code=201)
def generate_blog(
    request: BlogGenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate a new blog post using AI"""
    
    try:
        # Generate blog content
        result = hf_service.generate_blog(
            topic=request.topic,
            tone=request.tone,
            length=request.length,
            keywords=request.keywords
        )
        
        # Save to database
        blog_post = BlogPost(
            topic=request.topic,
            tone=request.tone,
            length=request.length,
            keywords=request.keywords,
            title=result["title"],
            content=result["content"],
            word_count=result["word_count"],
            seo_score=result["seo_score"]
        )
        
        db.add(blog_post)
        db.commit()
        db.refresh(blog_post)
        
        return blog_post
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blogs", response_model=BlogListResponse)
def list_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of all generated blogs"""
    
    total = db.query(BlogPost).count()
    blogs = (
        db.query(BlogPost)
        .order_by(BlogPost.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return {"total": total, "blogs": blogs}

@router.get("/blogs/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Get a specific blog by ID"""
    
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog

@router.delete("/blogs/{blog_id}", response_model=MessageResponse)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    """Delete a blog post"""
    
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    
    return {"message": "Blog deleted successfully"}