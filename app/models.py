from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
  __tablename__ = 'posts'

  owner_id = Column(BigInteger, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
  id = Column(BigInteger, primary_key = True, nullable = False)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  time = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
  owner = relationship("User")

class User(Base):
  __tablename__ = 'users'

  username = Column(String, nullable = False, server_default = "user")
  email = Column(String, nullable = False, unique = True)
  password = Column(String, nullable = False)
  id = Column(BigInteger, primary_key = True, nullable = False)
  time = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class Vote(Base):
  __tablename__ = 'votes'

  user_id = Column(BigInteger, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
  post_id = Column(BigInteger, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True, nullable = False)