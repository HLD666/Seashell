import time
import random
import json
import jsonpath
from selenium import webdriver
from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from spider.spider_config import SPIDER_DB_URI
from spider.independent.spider_hotlist.spider_configs import request_retry_number
from spider.independent.spider_hotlist.models import create_dst_model, create_src_model

# from crawl import Crawler


"""
京东商品排行榜爬虫
从网页中获取分类、榜单名称、链接参数（type_name, min_type_name, cateid）
传入selenium，selenium返回数据
返回数据存入数据库（type_name，min_type_name，current_rank，ware_name，jd_price，good_str，img_path）
"""


class SeleniumjdSpider:
    def __init__(self, spider_id, src_table, dst_table):
        self.spider_id = spider_id
        self.src_table = src_table
        self.dst_table = dst_table
        print(self.spider_id, self.src_table, self.dst_table)

        self.SrcDbModel = None
        self.DstDbModel = None

        self.session = None
        self.driver = None

    def get_url(self):
        """请求主页面"""
        self.driver.get('https://www.jd.com/')
        self.driver.implicitly_wait(5)
        time.sleep(3)
        # print("扫码登录中")
        # time.sleep(10)

    def window_switching_new(self):
        """切换到新窗口（弹出新窗口，则关闭前一个窗口，控制新窗口）"""
        handles = self.driver.window_handles
        print("当前窗口句柄", handles)
        time.sleep(1.5)
        if len(handles) == 1:
            handle_run = handles[0]
            self.driver.switch_to.window(handle_run)
        else:
            handle_run = handles[1]
            self.driver.close()
            self.driver.switch_to.window(handle_run)
            time.sleep(4)

    def ranking_list(self):
        """
        进入排行榜
        """
        # 页面下拉加载数据
        for z in range(0, 3):
            self.driver.execute_script("var q=document.documentElement.scrollTop=" + str(z * 800))
            time.sleep(random.uniform(0.45, 0.75))
        # 将下拉滑动条滑动到指定区域
        self.driver.execute_script("arguments[0].scrollIntoView();",
                                   self.driver.find_element_by_xpath('//*[@id="J_niceGoods"]'))
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="J_top"]/div[1]/a/i').click()
        time.sleep(0.5)

    def unfold_ranking_list_1(self):
        """获取展开后排行榜1  大分类名称  小分类名称  链接"""
        zhu_tree_1 = self.driver.find_elements_by_xpath('//div[@class="top_mod_key tmk"]/ul')
        list_1 = []
        for li in zhu_tree_1:
            type_name = li.find_element_by_xpath('.').get_attribute('data-catename')
            zhu_tree_2 = li.find_elements_by_xpath('./li/a')
            for li_2 in zhu_tree_2:
                min_type_name = li_2.get_attribute('text')
                cateid = li_2.get_attribute('data-cateid')
                print(type_name, min_type_name, cateid)
                list_1.append([type_name, min_type_name, cateid])
            time.sleep(random.uniform(0.15, 0.75))
        return list_1

    def unfold_ranking_list_2(self):
        """获取展开后排行榜2  大分类名称  小分类名称  链接"""
        zhu_tree = self.driver.find_elements_by_xpath('//ul[@class="tmca_fstcls"]/li')
        list_2 = []
        for li in zhu_tree:
            type_name = li.find_element_by_xpath('./a').get_attribute('text')
            type_id = li.find_element_by_xpath('./a').get_attribute('data-cateid')
            zhu_tree_2 = self.driver.find_elements_by_xpath(
                '//div[@class="tmca_scdcls tmca_scdcls_' + str(type_id) + '"]/div/div/ul/li/a')
            for li_2 in zhu_tree_2:
                min_type_name = li_2.get_attribute('text')
                cateid = li_2.get_attribute('data-cateid')
                print(type_name, min_type_name, cateid)
                list_2.append([type_name, min_type_name, cateid])
        time.sleep(random.uniform(0.15, 0.75))
        return list_2

    def get_src(self):
        """查询deom_src表所有关键字"""
        return self.session.query(self.SrcDbModel.type_name, self.SrcDbModel.min_type_name,
                                  self.SrcDbModel.cateid).all()

    def get_type_url(self, cateid):
        """请求分类排行榜页面"""
        type_name_url = "https://ch.jd.com/hotsale?cateId={}".format(cateid)
        self.driver.get(type_name_url)
        self.driver.implicitly_wait(8)
        time.sleep(2)

    @retry(stop_max_attempt_number=request_retry_number)  # 请求重试request_retry_number次
    def get_data_list(self, type_name, min_type_name):
        """获得小分类排行榜json数据"""
        datas = self.driver.find_element_by_xpath("//*").text
        datas = json.loads(datas, encoding='utf8')
        type_name = type_name  # 大分类名称
        min_type_name = min_type_name  # 小分类名称
        current_rank = jsonpath.jsonpath(datas, '$..currentRank')  # 排名
        ware_name = jsonpath.jsonpath(datas, '$..wareName')  # 名称
        jd_price = jsonpath.jsonpath(datas, '$..jdPrice')  # 价格
        good_str = jsonpath.jsonpath(datas, '$..GoodCountStr')  # 关注数
        img_path = jsonpath.jsonpath(datas, '$..imgPath')  # 图片
        min_num = min(len(current_rank), len(ware_name), len(jd_price), len(good_str), len(img_path))
        data_list = []
        for i in range(0, min_num):
            col_datas = dict()
            col_datas['type_name'] = type_name
            col_datas['min_type_name'] = min_type_name
            col_datas['current_rank'] = current_rank[i]
            col_datas['ware_name'] = ware_name[i]
            col_datas['jd_price'] = jd_price[i]
            col_datas['good_str'] = good_str[i]
            col_datas['img_path'] = img_path[i]
            print(col_datas)
            data_list.append(col_datas)
        return data_list

    def save_data(self, data_list):
        """数据入库"""
        for data in data_list:
            target = self.DstDbModel(**data)
            self.session.add(target)
            self.session.commit()

    def start(self):
        self.SrcDbModel = create_src_model(self.src_table)
        self.DstDbModel = create_dst_model(self.dst_table)
        engine = create_engine(SPIDER_DB_URI)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        option = webdriver.ChromeOptions()  # 创建浏览器
        # option.binary_location = "/usr/lib64/chromium-browser/headless_shell"
        # option.add_argument("--remote-debugging-port=9222")
        option.headless = True  # do not open UI
        option.add_argument('disable-infobars')  # 关闭提示信息
        prefs = {"safebrowsing.enabled": True, 'profile.managed_default_content_settings.images': 2}  # 不提示安全警告, 不显示图片
        option.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=option, desired_capabilities=None)
        self.driver.set_window_size(1366, 768)  # 设置窗口大小

        # rows = self.get_src()
        # print(rows)
        # for row in rows:
        self.get_url()
        self.ranking_list()
        self.window_switching_new()
        row_lists = self.unfold_ranking_list_1() + self.unfold_ranking_list_2()
        print(row_lists)
        for row in row_lists[0:5]:
            self.get_type_url(row[2])
            try:
                try:
                    data_list = self.get_data_list(row[0], row[1])
                except:
                    self.driver.refresh()  # 重试都失败后刷新
                    data_list = self.get_data_list(row[0], row[1])
            except:
                # 刷新失败跳过
                continue
            self.save_data(data_list)
            time.sleep(2)
        self.driver.quit()
