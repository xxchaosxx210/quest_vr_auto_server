from sqlalchemy import (
    String,
    TIMESTAMP,
    Integer,
    Column,
    Float,
    func
)

import database


class Games(database.Base):

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, primary_key=False, nullable=False)
    magnet = Column(String, primary_key=False, nullable=False)
    version = Column(Float, primary_key=False, nullable=False, default=1.0)
    filesize = Column(Integer, primary_key=False, nullable=False, default=0)
    date_added = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
