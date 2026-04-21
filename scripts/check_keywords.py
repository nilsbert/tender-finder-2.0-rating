import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import db
from core.repository import RatingRepository

async def check():
    async with db.session_factory() as session:
        async with session.begin():
            repo = RatingRepository(session)
            keywords = await repo.get_all_keywords()
            print(f"Total Keywords: {len(keywords)}")
            if keywords:
                print("First 5 keywords:")
                for kw in keywords[:5]:
                    print(f" - {kw.term} ({kw.weight})")

if __name__ == "__main__":
    asyncio.run(check())
