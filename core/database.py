import os
import urllib.parse
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from models.orm import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, schema_name):
        self.schema = schema_name
        # Prioritize DATABASE_URL for E2E tests and Docker flexibility
        self.url = os.getenv("DATABASE_URL")
        
        if not self.url:
            conn_str = os.getenv("MSSQL_CONNECTION_STRING")
            if not conn_str:
                self.url = f"sqlite+aiosqlite:///{schema_name}.db"
            else:
                self.url = self._convert_odbc_to_url(conn_str)
        
        self.engine = create_async_engine(self.url, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    def _convert_odbc_to_url(self, conn_str: str) -> str:
        if conn_str.startswith("Driver={"):
            parts = {}
            for part in conn_str.split(';'):
                if '=' in part:
                    k, v = part.split('=', 1)
                    parts[k.strip()] = v.strip()
            driver = parts.get('Driver', '').replace('{', '').replace('}', '')
            server = parts.get('Server', '').replace('tcp:', '').split(',')[0]
            database = parts.get('Database', '')
            
            uid = parts.get('Uid', '')
            pwd = parts.get('Pwd', '').replace('{', '').replace('}', '')
            encoded_pwd = urllib.parse.quote_plus(pwd)
            return f"mssql+aioodbc://{uid}:{encoded_pwd}@{server}/{database}?driver={driver}&TrustServerCertificate=yes"
        return conn_str

    async def get_session(self):
        """Standard provisioner for FastAPI Depends()"""
        async with self.session_factory() as session:
            yield session

    async def init_db(self):
        """Initialize database schema and tables with better error handling and logging."""
        logger.info(f"🔄 Initializing {self.schema} database at: {self.url}")
        
        # Ensure tables are registered
        from models.orm import Base
        logger.info(f"📋 Registered tables for {self.schema}: {list(Base.metadata.tables.keys())}")

        if "sqlite" in self.url:
            for table in Base.metadata.tables.values():
                table.schema = None
        
        try:
            async with self.engine.begin() as conn:
                if "mssql" in self.url:
                    await conn.execute(text(f"IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{self.schema}') EXEC('CREATE SCHEMA {self.schema}')"))
                await conn.run_sync(Base.metadata.create_all)
            logger.info(f"✅ {self.schema} database initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize {self.schema} database: {e}", exc_info=True)
            raise

# Note: All Keyword domain methods (get_keywords, save_keyword, etc.) 
# have been moved to RatingRepository for better DDD and DRY compliance.

db = DatabaseManager("rating")
