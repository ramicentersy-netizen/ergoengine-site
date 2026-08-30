from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .database import Base

class IntentLevel(str, enum.Enum):
    INFORMATIONAL = "informational"
    COMMERCIAL_INVESTIGATION = "commercial_investigation"
    TRANSACTIONAL = "transactional"

class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    PUBLISHED = "published"
    REJECTED = "rejected"
    FLAGGED_FOR_UPDATE = "flagged_for_update"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    affiliate_url = Column(String(500), nullable=False)
    affiliate_source = Column(String(50), default="Amazon Associates")
    rating = Column(Float, default=4.5)
    pros_json = Column(Text, nullable=False)
    cons_json = Column(Text, nullable=False)
    specs_json = Column(Text, nullable=False)
    ideal_for = Column(String(255), nullable=False)
    avoid_if = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    clicks = relationship("AffiliateClick", back_populates="product")

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(255), unique=True, index=True, nullable=False)
    cluster = Column(String(100), nullable=False)
    intent = Column(SQLEnum(IntentLevel), default=IntentLevel.COMMERCIAL_INVESTIGATION)
    search_volume = Column(Integer, default=500)
    keyword_difficulty = Column(Float, default=30.0)
    is_targeted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    article_type = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    meta_description = Column(String(300), nullable=False)
    content_html = Column(Text, nullable=False)
    schema_json = Column(Text, nullable=True)
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)
    word_count = Column(Integer, default=0)
    reading_time_minutes = Column(Integer, default=3)
    target_keyword = Column(String(255), nullable=False)
    page_views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    clicks = relationship("AffiliateClick", back_populates="article")

class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    cta_placement = Column(String(50), nullable=False)
    user_ip_hash = Column(String(64), nullable=True)
    referrer = Column(String(255), nullable=True)
    converted = Column(Boolean, default=False)
    commission_earned = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="clicks")
    article = relationship("Article", back_populates="clicks")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
