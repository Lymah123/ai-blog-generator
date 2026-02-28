import pytest
from unittest.mock import patch, MagicMock


class TestBlogRoutes:
    """Integration tests for blog API endpoints"""

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    @patch('app.services.ai_service.hf_service.generate_blog')
    def test_generate_blog_success(self, mock_generate, client, sample_blog_data):
        """Test successful blog generation"""
        # Mock AI service response
        mock_generate.return_value = {
            "title": "Generated Blog Title",
            "content": "Generated content here",
            "word_count": 100,
            "seo_score": 75.0
        }
        
        response = client.post("/api/v1/generate", json=sample_blog_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Generated Blog Title"
        assert data["topic"] == sample_blog_data["topic"]
        assert data["seo_score"] == 75.0

    def test_generate_blog_missing_topic(self, client):
        """Test blog generation with missing topic"""
        invalid_data = {
            "tone": "professional",
            "length": "medium"
        }
        
        response = client.post("/api/v1/generate", json=invalid_data)
        
        assert response.status_code == 422  # Validation error

    def test_generate_blog_invalid_tone(self, client):
        """Test blog generation with invalid data"""
        invalid_data = {
            "topic": "Test",
            "tone": "",  # Empty tone
            "length": "medium"
        }
        
        response = client.post("/api/v1/generate", json=invalid_data)
        
        assert response.status_code in [400, 422]

    def test_list_blogs_empty(self, client):
        """Test listing blogs when database is empty"""
        response = client.get("/api/v1/blogs")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["blogs"] == []

    def test_list_blogs_with_data(self, client, sample_blog_post):
        """Test listing blogs with data"""
        response = client.get("/api/v1/blogs")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["blogs"]) == 1
        assert data["blogs"][0]["id"] == sample_blog_post.id

    def test_list_blogs_pagination(self, client, db_session):
        """Test blog listing with pagination"""
        from app.models.blog import BlogPost
        
        # Create 5 blogs
        for i in range(5):
            blog = BlogPost(
                topic=f"Topic {i}",
                tone="professional",
                length="medium",
                keywords="test",
                title=f"Title {i}",
                content=f"Content {i}",
                word_count=100,
                seo_score=70.0
            )
            db_session.add(blog)
        db_session.commit()
        
        # Test pagination
        response = client.get("/api/v1/blogs?skip=0&limit=3")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["blogs"]) == 3

    def test_get_blog_success(self, client, sample_blog_post):
        """Test getting a specific blog"""
        response = client.get(f"/api/v1/blogs/{sample_blog_post.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_blog_post.id
        assert data["topic"] == sample_blog_post.topic

    def test_get_blog_not_found(self, client):
        """Test getting non-existent blog"""
        response = client.get("/api/v1/blogs/99999")
        
        assert response.status_code == 404

    def test_delete_blog_success(self, client, sample_blog_post):
        """Test deleting a blog"""
        response = client.delete(f"/api/v1/blogs/{sample_blog_post.id}")
        
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify deletion
        get_response = client.get(f"/api/v1/blogs/{sample_blog_post.id}")
        assert get_response.status_code == 404

    def test_delete_blog_not_found(self, client):
        """Test deleting non-existent blog"""
        response = client.delete("/api/v1/blogs/99999")
        
        assert response.status_code == 404

    @patch('app.services.ai_service.hf_service.generate_blog')
    def test_generate_blog_with_keywords(self, mock_generate, client):
        """Test blog generation with keywords"""
        mock_generate.return_value = {
            "title": "Test Title",
            "content": "Test content with python and fastapi keywords",
            "word_count": 100,
            "seo_score": 85.0
        }
        
        data = {
            "topic": "Python FastAPI",
            "tone": "technical",
            "length": "short",
            "keywords": "python, fastapi, api"
        }
        
        response = client.post("/api/v1/generate", json=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["keywords"] == data["keywords"]

    @patch('app.services.ai_service.hf_service.generate_blog')
    def test_generate_blog_all_tones(self, mock_generate, client):
        """Test blog generation with all tone options"""
        mock_generate.return_value = {
            "title": "Test",
            "content": "Content",
            "word_count": 50,
            "seo_score": 70.0
        }
        
        tones = ["professional", "casual", "technical", "educational"]
        
        for tone in tones:
            data = {
                "topic": f"Test {tone}",
                "tone": tone,
                "length": "short"
            }
            
            response = client.post("/api/v1/generate", json=data)
            
            assert response.status_code == 201
            assert response.json()["tone"] == tone

    @patch('app.services.ai_service.hf_service.generate_blog')
    def test_generate_blog_all_lengths(self, mock_generate, client):
        """Test blog generation with all length options"""
        mock_generate.return_value = {
            "title": "Test",
            "content": "Content",
            "word_count": 100,
            "seo_score": 70.0
        }
        
        lengths = ["short", "medium", "long"]
        
        for length in lengths:
            data = {
                "topic": f"Test {length}",
                "tone": "professional",
                "length": length
            }
            
            response = client.post("/api/v1/generate", json=data)
            
            assert response.status_code == 201
            assert response.json()["length"] == length