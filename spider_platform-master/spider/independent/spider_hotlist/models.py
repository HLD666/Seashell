from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime
Base = declarative_base()


def create_src_model(table_anme):
    class JdSearchSrcModel(Base):
        print("查询数据表", table_anme)
        __tablename__ = table_anme
        type_name = Column(String(100))
        min_type_name = Column(String(100))
        cateid = Column(String(50), primary_key=True)

    return JdSearchSrcModel


def create_dst_model(table_anme):
    class JdSearchDstModel(Base):
        print("存入数据表", table_anme)
        __tablename__ = table_anme
        type_name = Column(String(100), primary_key=True)
        min_type_name = Column(String(100), primary_key=True)
        current_rank = Column(String(50), primary_key=True)
        ware_name = Column(String(300))
        jd_price = Column(String(50))
        good_str = Column(String(50))
        img_path = Column(String(300))

    return JdSearchDstModel
