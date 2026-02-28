import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.blog import BlogPost

# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_blog_data():
    """Sample blog data for testing"""
    return {
        "topic": "Test Blog Topic",
        "tone": "professional",
        "length": "medium",
        "keywords": "test, python, fastapi"
    }


@pytest.fixture
def sample_blog_post(db_session):
    """Create a sample blog post in the database"""
    blog = BlogPost(
        topic="Sample Topic",
        tone="professional",
        length="medium",
        keywords="test, sample",
        title="Sample Blog Title",
        content="This is sample blog content for testing.",
        word_count=8,
        seo_score=75.0
    )
    db_session.add(blog)
    db_session.commit()
    db_session.refresh(blog)
    return blog