import asyncio
import os
import sys

# Add the project root to sys.path to allow imports from rating
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "rating")))

from core.database import db
from models.orm import ConfigRatingORM


async def seed():
    print("🚀 Initializing rating database...")
    await db.init_db()

    async with db.session_factory() as session, session.begin():
        print("🌱 Seeding rating configuration...")
        # Check if exists
        res = await session.execute(ConfigRatingORM.__table__.select().where(ConfigRatingORM.id == 1))
        if not res.fetchone():
            cfg = ConfigRatingORM(
                id=1,
                overall_score_threshold=50,
                title_score_threshold=12,
                version=1
            )
            session.add(cfg)
            print("✅ Seeding complete!")
        else:
            print("⚠️ Rating config already exists, skipping.")

if __name__ == "__main__":
    asyncio.run(seed())
