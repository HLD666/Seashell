import json
import re
from urllib.parse import quote
from spider.standard.base.asyn_spider import AsynSpider
from urllib import parse
import pymysql
import random


def get_cookies():
    con_engine = pymysql.connect(host='192.168.7.247', user='admin', password='1q2w3e4r', database='crl_res', port=3306,
                                 charset='utf8')
    cursor = con_engine.cursor()

    sql_ = "SELECT cookie FROM `crl_res`.`tb_toutiao_cookies`"

    try:
        cursor.execute(sql_)
        #获得cookies元组
        results = cursor.fetchall()
        cookies = list()
        for row in results:
            cookie = str(row[0])
            cookies.append(cookie)
        return cookies
    except Exception as e:
        print("数据读取失败",e)

    con_engine.close()

cookies = get_cookies()

def filter_emoji(desstr):
    '''
    将表情包替换成字符串'[emoji]'
    :param desstr:
    :return:
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub('[emoji]', desstr)


class JdSreachSpider(AsynSpider):
    def make_url_info(self, row):
        keyword = quote(row.keyword)
        url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=' \
              '{keyword}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp='.format(
            keyword=keyword)
        url_info = {
            'keyword': keyword,
            'url': url,
            'offset': 0,
            'Cookie': random.choice(cookies),
            'is_generate': True
        }

        self.url_queue.put(url_info)

    def page_parse(self, html, url_info):
        try:
            html = filter_emoji(html)
            #print(html)
            jdata = json.loads(html)
            items = jdata['data']
        except Exception as e:
            print("%s json解析失败失败：%s" % (url_info['sourceId'], str(e)))
            return []

        generate_info = {'page_num':'120'}

        data_list = list()

        if items != None:
            for item in items:
                item_info = dict()
                if 'abstract' in item:
                    try:
                        keyword = parse.unquote(item['keyword'])
                        if keyword == '腾讯':
                            num = 1
                        if keyword == '网易':
                            num = 2
                        if keyword == '华为':
                            num = 3
                        item_info['keyword_id'] = num
                        item_info['title'] = item['title']
                        item_info['article_url'] = 'https://www.toutiao.com' + item['open_url']
                        item_info['author'] = item['media_name']
                        item_info['author_url'] = item['media_url']
                        item_info['release_time'] = item['datetime']
                        item_info['comment_counts'] = item['comment_count']
                        data_list.append(item_info)
                    except:
                        print('----------抓到的不是搜索结果----------')
                else:
                    pass
        else:
            pass

        return data_list, generate_info

    def generate_page(self, url_info, generate_info):
        if 'page_num' in generate_info.keys():
            page_num = int(generate_info['page_num'])
        else:
            return []

        keyword = url_info['keyword']
        for offset in range(20, page_num + 1, 20):
            new_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={offset}&format=json&keyword={keyword}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp='.format(
                offset=offset, keyword=keyword)
            url_info = {
                'keyword': keyword,
                'url': new_url,
                'offset': offset,
                'Cookie': random.choice(cookies),
                'is_generate': False
            }

            self.url_queue.put(url_info)


if __name__ == "__main__":
    A = JdSreachSpider(5, 'para_example_5', 'res_toutiao_search')
    A.start()
