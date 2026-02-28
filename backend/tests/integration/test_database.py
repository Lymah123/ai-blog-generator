import pytest
from app.models.blog import BlogPost


class TestDatabaseOperations:
    """Test database CRUD operations"""

    def test_create_blog_post(self, db_session):
        """Test creating a blog post"""
        blog = BlogPost(
            topic="Test Topic",
            tone="professional",
            length="medium",
            keywords="test",
            title="Test Title",
            content="Test content",
            word_count=2,
            seo_score=75.0
        )
        
        db_session.add(blog)
        db_session.commit()
        db_session.refresh(blog)
        
        assert blog.id is not None
        assert blog.topic == "Test Topic"

    def test_read_blog_post(self, db_session, sample_blog_post):
        """Test reading a blog post"""
        blog = db_session.query(BlogPost).filter(
            BlogPost.id == sample_blog_post.id
        ).first()
        
        assert blog is not None
        assert blog.topic == sample_blog_post.topic

    def test_update_blog_post(self, db_session, sample_blog_post):
        """Test updating a blog post"""
        sample_blog_post.title = "Updated Title"
        db_session.commit()
        
        updated_blog = db_session.query(BlogPost).filter(
            BlogPost.id == sample_blog_post.id
        ).first()
        
        assert updated_blog.title == "Updated Title"

    def test_delete_blog_post(self, db_session, sample_blog_post):
        """Test deleting a blog post"""
        blog_id = sample_blog_post.id
        
        db_session.delete(sample_blog_post)
        db_session.commit()
        
        deleted_blog = db_session.query(BlogPost).filter(
            BlogPost.id == blog_id
        ).first()
        
        assert deleted_blog is None

    def test_query_blogs_by_tone(self, db_session):
        """Test querying blogs by tone"""
        # Create blogs with different tones
        for tone in ["professional", "casual", "technical"]:
            blog = BlogPost(
                topic=f"Topic {tone}",
                tone=tone,
                length="medium",
                title=f"Title {tone}",
                content="Content",
                word_count=1,
                seo_score=70.0
            )
            db_session.add(blog)
        db_session.commit()
        
        professional_blogs = db_session.query(BlogPost).filter(
            BlogPost.tone == "professional"
        ).all()
        
        assert len(professional_blogs) == 1
        assert professional_blogs[0].tone == "professional"

    def test_blog_timestamps(self, db_session):
        """Test that created_at timestamp is set"""
        blog = BlogPost(
            topic="Test",
            tone="professional",
            length="medium",
            title="Test",
            content="Content",
            word_count=1,
            seo_score=70.0
        )
        
        db_session.add(blog)
        db_session.commit()
        db_session.refresh(blog)
        
        assert blog.created_at is not None