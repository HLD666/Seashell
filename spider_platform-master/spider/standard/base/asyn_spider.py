import asyncio
import queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from spider.spider_config import SPIDER_DB_URI
from spider.standard.base.models import src_model_dict, dst_model_dict
from spider.standard.base.crawl import Crawler


class AsynSpider:
    def __init__(self, spider_id, src_table, dst_table):
        self.configs = {
            'max_times': 10,
            'timeout': 5,
        }

        self.coro_num = 3
        self.spider_id = spider_id
        self.src_table = src_table
        self.dst_table = dst_table
        self.url_queue = None
        self.SrcDbModel = None
        self.DstDbModel = None
        self.session = None
        self.Crawler = None

    def get_src(self):
        return self.session.query(self.SrcDbModel).all()

    def make_url_info(self, row):
        return []

    def start(self):
        self.url_queue = queue.Queue()
        self.SrcDbModel = src_model_dict[self.spider_id](self.src_table)
        self.DstDbModel = dst_model_dict[self.spider_id](self.dst_table)
        engine = create_engine(SPIDER_DB_URI)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.Crawler = Crawler

        rows = self.get_src()
        for row in rows:
            url_info = self.make_url_info(row)
            self.url_queue.put(url_info)

        crawlers = [Crawler(self.url_queue, self.page_parse, self.save_data, self.generate_page) for _ in range(0, self.coro_num)]
        loop = asyncio.new_event_loop()
        # loop = asyncio.get_event_loop()
        to_do = [crawlers[coro_id].asyn_crawl(coro_id) for coro_id in range(0, self.coro_num)]
        wait_coro = asyncio.wait(to_do)
        loop.run_until_complete(wait_coro)
        loop.run_until_complete(asyncio.sleep(0.25))
        loop.close()

    def page_parse(self, html, url_info):
        return [], None

    def save_data(self, data_list):
        for data in data_list:
            for key in data.keys():
                if isinstance(data[key], list):
                    data[key] = str(data[key])

            try:
                target = self.DstDbModel(**data)
                self.session.add(target)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print(str(e))
                pass

    def generate_page(self, url_info, generate_info):
        return []
