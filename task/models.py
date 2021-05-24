from sqlalchemy import create_engine, Float, Column, Integer, String, Boolean, ForeignKey, update, \
    Unicode, or_, and_, DateTime, literal, JSON, Text, DECIMAL, BIGINT, Table, Sequence, Date, cast, func
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from datetime import datetime, timedelta
from sqlalchemy.sql import case
from datetime import datetime

Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True)
    currency = Column(String(250), nullable=False)
    sum = Column(String(250), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(250), nullable=True)




