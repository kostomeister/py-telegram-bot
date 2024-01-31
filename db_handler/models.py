from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Reports(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    location = Column(String(255))
    checklist = Column(String(255))
    comment = Column(Text)
    photo_url = Column(Text, nullable=True)
