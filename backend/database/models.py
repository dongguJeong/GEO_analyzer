from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from database.database import Base


class Analysis(Base):

    __tablename__ = "analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    url = Column(String)

    score = Column(Float)

    grade = Column(String)