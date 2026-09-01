import os
import time
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    LargeBinary,
    Float,
    func,
    Boolean,
)

from sqlalchemy.orm import sessionmaker, relationship
import bcrypt

from sqlalchemy.ext.declarative import declarative_base


import streamlit as st

# Retrieve credentials securely
db_config = st.secrets["db_credentials"]

# Example connecting via Streamlit's SQL connection wrapper
conn = st.connection(
    "sql",
    url=f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
)


# The engine handles raw communications with your remote Supabase database instance cluster
engine = create_engine(
    conn,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Automatically checks if your Supabase connection is still alive before querying
)


engine = st_conn.driver

# 2. Bind it cleanly to your sessionmaker factory helper
# ✅ This permanently solves your ArgumentError and UnboundExecutionError bugs!
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db_session():
    """
    Helper function to safely spin up a fully bound database connection session
    """
    db_session = SessionLocal()
    try:
        return db_session
    except Exception as e:
        db_session.close()
        raise e


# =========================================================================
# 👤 PROFILE TABLE SCHEMA (PRIMARY LOG DETAILS MATRIX CHANNELS)
# ========================================================================


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    studio_name = Column(String, nullable=False)
    biography = Column(String, default="No corporate profile log attached yet.")
    profile_picture_name = Column(String, default="default_profile.png")
    created_at = Column(DateTime, default=datetime.utcnow)
    # 🔥 NEW SUBSCRIPTION MANAGEMENT METRIC LAYERS 🔥
    # Default newly registered ateliers to the unconflicted "freemium" layer tier
    subscription_tier = Column(String, nullable=False, default="freemium")
    monthly_generation_count = Column(Integer, nullable=False, default=0)
    cycle_reset_timestamp = Column(DateTime, default=func.now(), nullable=False)

    # Establish relational back-references to tracking items
    collections = relationship(
        "Collection", back_populates="owner", cascade="all, delete-orphan"
    )
    orders = relationship(
        "ShopOrder", back_populates="buyer", cascade="all, delete-orphan"
    )


# =========================================================================
# 📁 NEW: FABRIC COLLECTIONS DATABASE TABLE SCHEMA
# =========================================================================
class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    studio_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    origin = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    raw_images_blob = Column(
        LargeBinary, nullable=True
    )  # Stores multiple files encoded cleanly as byte strings
    date = Column(
        String(100), default=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    )

    owner = relationship("User", back_populates="collections")


# =========================================================================
# 🛒 NEW: WHOLESALE TEXTILE SHOP ORDER LOG TABLE SCHEMA
# =========================================================================


class ShopOrder(Base):
    __tablename__ = "shop_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    studio_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    item_title = Column(String(255), nullable=False)
    details = Column(String(255), nullable=False)
    cost = Column(
        Float, nullable=False, default=0.0
    )  # 🔥 NEW: Tracks true numerical monetary price metrics
    status_tag = Column(String(100), default="Allocation Slot Locked / Order Processed")
    created_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("User", back_populates="orders")


# =========================================================================
# 📦 RELATIONAL SCHEMA EXTENSION: CLIENT SPECIFICATIONS TABLE (DATABASE.PY)
# =========================================================================


# =========================================================================
# 🧵 FIX: COMPATIBLE TIMESTAMPMATRIX COLUMN FOR MODERN SQLALCHEMY (DATABASE.PY) 🧵
# =========================================================================


class ClientMeasurement(Base):
    __tablename__ = "client_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    client_name = Column(String, nullable=False, default="Unnamed Client Fit")
    bust_dimension = Column(Float, nullable=False)
    waist_dimension = Column(Float, nullable=False)
    hips_dimension = Column(Float, nullable=False)
    garment_length = Column(Float, nullable=False)
    settlement_currency = Column(String, nullable=False, default="USD ($)")
    final_cost_valuation = Column(Float, nullable=False)

    # 🔥 FIX: Using func.now() delegates the timestamp creation directly to the
    # engine. This removes the lambda wrapper and completely avoids the TypeError!
    creation_timestamp = Column(DateTime, default=func.now(), nullable=False)


# Append this class directly to your database file (database.py)
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func


class ClientSpecification(Base):
    """
    PostgreSQL Database Ledger Model.
    Tracks premium designer atelier client fitting specifications,
    measurement metrics proportions, and marketplace commercial invoice data rows.
    """

    __tablename__ = "client_specifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, index=True, nullable=False
    )  # Maps to the executing designer session id
    client_name = Column(String(255), index=True, nullable=False)
    style_cut = Column(String(100), nullable=True)  # e.g. gown, jumpsuit, jacket

    # Precise physical measurement matrix proportions metrics columns
    chest = Column(Float, default=0.0)
    waist = Column(Float, default=0.0)
    hips = Column(Float, default=0.0)
    length = Column(Float, default=0.0)
    shoulder = Column(Float, default=0.0)

    # Financial data variables settlement metrics columns
    total_invoice = Column(Float, default=0.0)
    status = Column(
        String(50), default="Unpaid Draft"
    )  # e.g. Unpaid Draft, Deposit Received, Fully Settled
    notes = Column(Text, nullable=True)

    # Persistent global creation audit tracking stamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


# Ensure tables are compiled automatically upon next launch initialization loop
# Base.metadata.create_all(bind=engine)


class ShopProduct(Base):
    """
    Table tracking user-created products, marketplace sales volumes,
    and detailed storefront configuration parameters.
    """

    __tablename__ = "shop_products"

    # Core Identifiers
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    product_title = Column(String, nullable=False, default="Untitled Item")

    # Dashboard Analytical Vectors
    total_units_sold = Column(Integer, nullable=False, default=0)
    # gross_revenue_accrued = Column(Float, nullable=False, default=0.0)

    # Storefront Card Specifications
    retail_valuation_usd = Column(Float, nullable=False, default=0.0)
    additional_metadata = Column(
        Text, nullable=True
    )  # Used for dynamic descriptions or JSON strings
    attach_profile_badge = Column(Boolean, nullable=False, default=False)
    cached_b64_render = Column(
        Text, nullable=True
    )  # Stores base64 image strings safely


class CollectionWork(Base):
    """
    Join/Child table mapping individual design works or product variants
    to their designated parent user collections.
    """

    __tablename__ = "collection_works"

    id = Column(Integer, primary_key=True, index=True)

    # Connects the work entry to its parent collection row
    collection_id = Column(Integer, index=True, nullable=False)

    # Core item information
    work_title = Column(String, nullable=False, default="Untitled Work")
    work_status = Column(
        String, nullable=False, default="draft"
    )  # e.g., draft, active, archived

    # Optional formatting anchors
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TryOnPermission(Base):
    """
    Tracks microtransactions verifying if a specific user session
    has paid the flat fee required to run the AI try-on vector.
    """

    __tablename__ = "tryon_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)  # Customer ID
    product_id = Column(Integer, index=True, nullable=False)  # Product ID
    is_unlocked = Column(Boolean, default=False, nullable=False)
    stripe_session_id = Column(String, unique=True, nullable=True)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())


class UserUsageTracker(Base):
    """
    Tracks consumption limits across specialized server capabilities
    like free virtual try-on action windows.
    """

    __tablename__ = "user_usage_trackers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    tryon_execution_count = Column(Integer, default=0, nullable=False)
    has_unlocked_unlimited_paid = Column(Boolean, default=False, nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_fabric = Column(
        Boolean, default=False
    )  # True = Swatch roll, False = TryOn Eligible
    image_url = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)  # Search tag variables

    seller = relationship("User")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    status = Column(String(20), default="cart")  # cart, paid, cancelled
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    commission_paid = Column(Float, default=0.0)  # Separated platform split
    seller_payout = Column(Float, default=0.0)  # Net earnings to artisan
    stripe_session_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])
    product = relationship("Product")


class TryOnFeatureMeter(Base):
    __tablename__ = "tryon_feature_meters"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    free_uses_left = Column(Integer, default=5)
    has_premium_access = Column(Boolean, default=False)


class SellerProfile(Base):
    __tablename__ = "seller_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    brand_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    contact_phone = Column(String(30), nullable=True)
    payout_currency = Column(String(10), default="USD")  # Default studio setting

    user = relationship("User")


class DashboardProduct(Base):
    __tablename__ = "dashboard_products"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    raw_images_blob = Column(
        LargeBinary, nullable=True
    )  # Compressed lightweight representation
    origin = Column(String(50), default="Modern Afro-Futurism")

    # Commercial Tier Enhancements added by user on Dashboard
    price = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    notes = Column(Text, nullable=True)
    is_live_in_shop = Column(
        Boolean, default=False
    )  # Guard variable before final release push
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================================================================
# 🔐 CRYPTOGRAPHIC PASSWORD UTILITIES
# =========================================================================
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# def init_db():
#    Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#    init_db()
