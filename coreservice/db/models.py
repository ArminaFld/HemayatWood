from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)


    created_by = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
