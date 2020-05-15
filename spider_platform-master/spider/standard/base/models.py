from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime

Base = declarative_base()


def create_src_model1(table_anme):
    class JdReviewSrcModel(Base):
        __tablename__ = table_anme
        item_id = Column(String(50))
        page = Column(Integer)

    return JdReviewSrcModel


def create_dst_model1(table_anme):
    class JdReviewDstModel(Base):
        __tablename__ = table_anme
        item_id = Column(String(50))
        review_id = Column(String(50))
        create_time = Column(DateTime)
        buy_time = Column(DateTime)
        review_content = Column(String(1000))

    return JdReviewDstModel


def create_src_model2(table_anme):
    class JdSearchSrcModel(Base):
        __tablename__ = table_anme
        keyword = Column(String(50), primary_key=True)

    return JdSearchSrcModel


def create_dst_model2(table_anme):
    class JdSearchDstModel(Base):
        __tablename__ = table_anme
        shop_id = Column(String(50))
        shop_name = Column(String(300))
        item_id = Column(String(50), primary_key=True)

    return JdSearchDstModel


def create_src_model5(table_anme):
    class JdSearchSrcModel(Base):
        __tablename__ = table_anme
        id = Column(Integer)
        keyword = Column(String(255), primary_key=True)

    return JdSearchSrcModel


def create_dst_model5(table_anme):
    class JdSearchDstModel(Base):
        __tablename__ = table_anme
        keyword_id = Column(Integer)
        title = Column(String(255))
        article_url = Column(String(255), primary_key=True)
        author = Column(String(255))
        author_url = Column(String(255))
        release_time = Column(String(255))
        comment_counts = Column(Integer)

    return JdSearchDstModel


src_model_dict = {
    2: create_src_model1,
    1: create_src_model2,
    5: create_src_model5
}

dst_model_dict = {
    2: create_dst_model1,
    1: create_dst_model2,
    5: create_dst_model5
}
