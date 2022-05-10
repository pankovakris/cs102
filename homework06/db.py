from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

s = session()

# news = get_news("https://news.ycombinator.com/newest", 35)
# for new in news:
#     elem = News(
#         title = new['title'],
#         author=new['author'],
#         url = new['url'],
#         comments = new['comments'],
#         points = new['points'],
#     )
#     s.add(elem)
# s.commit()
