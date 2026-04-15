from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text
from models.orm import KeywordORM
from typing import List, Optional, Dict
import uuid

class RatingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_keywords(self) -> List[KeywordORM]:
        result = await self.session.execute(select(KeywordORM))
        return list(result.scalars().all())

    async def get_keyword_by_term(self, term: str) -> Optional[KeywordORM]:
        result = await self.session.execute(select(KeywordORM).where(KeywordORM.term == term))
        return result.scalars().first()

    async def get_keyword_by_id(self, keyword_id: str) -> Optional[KeywordORM]:
        result = await self.session.execute(select(KeywordORM).where(KeywordORM.id == keyword_id))
        return result.scalar_one_or_none()

    async def add_keyword(self, term: str, weight: float, type: str, 
                           category: Optional[str] = None, 
                           sub_type: Optional[str] = None, 
                           sub_category: Optional[str] = None,
                           id: Optional[str] = None) -> KeywordORM:
        keyword = KeywordORM(
            id=id or str(uuid.uuid4()),
            term=term,
            weight=weight,
            type=type,
            category=category,
            sub_type=sub_type,
            sub_category=sub_category
        )
        self.session.add(keyword)
        await self.session.flush()
        return keyword

    async def delete_keyword(self, keyword_id: str):
        await self.session.execute(delete(KeywordORM).where(KeywordORM.id == keyword_id))
        await self.session.flush()

    async def update_keyword(self, keyword_id: str, **kwargs) -> Optional[KeywordORM]:
        keyword = await self.get_keyword_by_id(keyword_id)
        if keyword:
            for key, value in kwargs.items():
                if hasattr(keyword, key):
                    setattr(keyword, key, value)
            await self.session.flush()
        return keyword

    async def get_categories(self) -> List[str]:
        stmt = text("SELECT DISTINCT sub_type FROM keywords WHERE sub_type IS NOT NULL")
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_keyword_tree(self) -> Dict[str, List[str]]:
        orms = await self.get_all_keywords()
        tree = {}
        for kw in orms:
            kw_type = kw.type or "Service"
            sub_type = kw.sub_type or "Unassigned"
            if kw_type not in tree:
                tree[kw_type] = set()
            tree[kw_type].add(sub_type)
        return {
            type_name: sorted(list(subtypes))
            for type_name, subtypes in tree.items()
        }
