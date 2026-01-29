from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print(f"🔗 连接数据库: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
print("✅ 数据库连接初始化成功！")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()