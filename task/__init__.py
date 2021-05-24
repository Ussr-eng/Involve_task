from flask import Flask, request, Response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configparser import ConfigParser
import os
from .models import Base

app = Flask(__name__)
app.config['SECRET_KEY'] = '99ehisip'

# engine = create_engine('sqlite:///test_task.db', connect_args={'check_same_thread': False})
engine = create_engine('sqlite:///test_task.db', connect_args={'check_same_thread': False}, convert_unicode=True)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from task import routes     # noqa: E402
