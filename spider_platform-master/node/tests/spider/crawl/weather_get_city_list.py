#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Scripts/External/weather_get_city_list.py
"""
    Get city list from www.yunlietou.com.
    Insert the city information into database.
"""

import re
import requests
from datetime import datetime
from lxml import etree
from urllib.parse import quote

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.exc import ProgrammingError, DataError, IntegrityError, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def result_table_creator(table_name):
    class CityListDB(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}

        id = Column(Integer(), primary_key=True)
        city_name = Column(String(50), unique=True)
        city_code = Column(String(50))
        flag = Column(Boolean())
        queried = Column(Boolean())
        update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

        def __repr__(self):
            return "CityList(city_name='{self.city_name}', " \
                   "city_code='{self.city_code}', " \
                   "flag='{self.flag}', " \
                   "queried='{self.queried}', " \
                   "update_time='{self.update_time}')".format(self=self)

        @staticmethod
        def from_dict(value):
            return CityListDB(city_name=value.get("city_name", None), city_code=value.get("city_code", None),
                              flag=value.get("flag", False), queried=value.get("queried", False))

    return CityListDB


def create_result_table(table_name, db_url):
    city_list_db_class = result_table_creator(table_name)
    print(city_list_db_class.__tablename__)

    engine = create_engine(db_url, pool_recycle=3600)
    Base.metadata.create_all(engine)


class CityList(object):
    search_url = "http://toy1.weather.com.cn/search?cityname={}&callback=success_jsonpCallback&_=1577150612080"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'close',
        'Cookie': 'Wa_lvt_1=1577091972,1577150612; Wa_lpvt_1=1577173931; csrfToken=cXFroy1yzhBYpGxGdZxmPSUr; Hm_lvt_26f859e26fb1d9afca60151d2d1fe304=1577173864; Hm_lpvt_26f859e26fb1d9afca60151d2d1fe304=1577173931; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1577173866; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1577173931; vjuids=-bdfceace7.16f36e3f39e.0.f4ed9d04b0ebe; vjlast=1577173906.1577173906.30',
        'Host': 'toy1.weather.com.cn',
        'Referer': 'http://www.weather.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    def __init__(self):
        self.city_list_db_class = None

        self.city_list = ["北京", "上海", "天津", "重庆", "海口", "三亚"]
        self.city_number_list = {}
        self.db = None
        self.session = None

    def get_the_web_page(self):
        try:
            city_list_result = requests.get("http://www.yunlietou.com/citylist.html")
        except TimeoutError as e:
            print(e)
        else:
            city_list_result_html = city_list_result.content
            etree_html = etree.HTML(city_list_result_html)
            etree.strip_tags(etree_html, "b")
            body = etree_html.xpath("/html/body/text()")
            body = [line.strip() for line in body if len(line.strip()) > 0]
            body = body[10:]

            for line in body:
                if line[-1] == "省" or line[-1] == "区" or "县级市" in line and "自治区直辖县级市" not in line:
                    continue
                else:
                    line = line.replace(".", "")
                    try:
                        line = line.split(":")[1]
                    except IndexError as e:
                        pass

                    lines = line.split(",")
                    for city_name in lines:
                        city_name = city_name.strip()
                        if " " in city_name:
                            continue
                        else:
                            self.city_list.append(city_name)
                            # print(city_name)

    def get_city_code_from_web(self, city):
        city_name_encode = quote(city)
        # print(city_name_encode)
        http_result = requests.get(self.search_url.format(city_name_encode),
                                   headers=self.headers)
        if http_result.status_code == 200:
            result_text = http_result.text
            result_re_match = re.search(r'\"\d+?~', str(result_text))
            try:
                result_text = result_re_match.group()
            except AttributeError as e:
                print(city)
                print(e)
            else:
                city_code = result_text[1:-1]
                self.city_number_list.update({city: city_code})

    def insert_the_city_into_database(self):
        for index, city_name in enumerate(self.city_list):
            city_dict = {"id": index, "city_name": city_name}
            try:
                city_dict["city_code"] = self.city_number_list[city_name]
            except KeyError:
                city_dict["flag"] = 0
            else:
                city_dict["flag"] = 1

            city_dict["queried"] = 1
            print(city_dict)

            self.implement_the_insert(city_dict)

    def implement_the_insert(self, data_get):
        data_get_db = self.city_list_db_class.from_dict(data_get)

        self.session.add(data_get_db)
        try:
            self.session.commit()
        except ProgrammingError as e:
            print(e)
        except IntegrityError as e:
            session.rollback()
            print(e)
        except DataError as e:
            print(e)

    def start(self, db_session, res_table_name, db_class=None):
        self.db = db_session

        if db_class is not None:
            self.city_list_db_class = db_class
            self.session = self.db
        else:
            self.city_list_db_class = result_table_creator(res_table_name)
            self.session = self.db.session

        self.get_the_web_page()
        print(len(self.city_list))

        for city_name in self.city_list:
            self.get_city_code_from_web(city_name)

        self.insert_the_city_into_database()


if __name__ == "__main__":
    result_table = "res_1_city_list"
    res_db = result_table_creator(result_table)

    db_url = "mysql+pymysql://admin:1q2w3e4r@localhost:3306/node_test?charset=utf8"
    engine = create_engine(db_url, pool_recycle=3600)
    Base.metadata.create_all(engine)

    session_mk = sessionmaker(bind=engine)
    session = session_mk()

    # data = {'id': 174, 'city_name': '通化', 'city_code': '101060501', 'flag': 1, 'queried': 1}
    # data_db = res_db.from_dict(data)
    #
    # session.add(data_db)
    # session.commit()

    city = CityList()
    city.start(session, result_table, res_db)
