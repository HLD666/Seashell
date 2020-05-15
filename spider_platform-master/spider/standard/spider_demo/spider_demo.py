import json
import re
from urllib.parse import quote
from spider.standard.base.asyn_spider import AsynSpider


def get_regex(regex, text, num):  # 获取对应的正则
    """
    @函数名：正则表达式匹配(匹配一个)
    @功能: 正则匹配，输出指定组的匹配结果
    """

    try:
        result = re.search(regex, text).group(num).strip()
    except:
        result = ''

    return result


def field_mapping(mapping_dict, src, dst):
    """
    @函数名：field_mapping
    @功能: 对源和目的字典进行字段对应，映射关系在mapping_dict中
    """

    for key in mapping_dict:
        if mapping_dict[key] in src.keys():
            dst[key] = src[mapping_dict[key]]

    return


class JdSreachSpider(AsynSpider):
    def make_url_info(self, row):
        keyword = quote(row.keyword)
        url = 'https://so.m.jd.com/ware/search._m2wq_list?keyword=' \
              '{keyword}&datatype=1&page=1&pagesize=100&&sort_type=sort_totalsales15_des'.format(keyword=keyword)
        url_info = {
            'keyword': keyword,
            'url': url,
            'page': 1
        }

        self.url_queue.put(url_info)

    def page_parse(self, html, url_info):
        try:
            # html = html.replace('\\x2F', '/').replace('\\x27', "'")
            html = html.replace('\\', '/')
            html = get_regex(r'searchCB\(([\s\S]*)\)', html, 1)
            jdata = json.loads(html)
            items = jdata['data']['searchm']['Paragraph']
        except Exception as e:
            print("%s json解析失败失败：%s" % (url_info['sourceId'], str(e)))
            return []

        generate_info = {}
        try:
            generate_info['page_num'] = jdata['data']['searchm']['Head']['Summary']['Page']['PageCount']
        except Exception as e:
            print("%s page不存在：%s" % (url_info['sourceId'], str(e)))

        data_list = list()
        mapping_dict = {
            "shop_id": "shop_id",
            "shop_name": "shop_name",
            "item_id": "wareid"
        }

        for item in items:
            item_info = dict()
            field_mapping(mapping_dict, item, item_info)

            data_list.append(item_info)

        return data_list, generate_info

    def generate_page(self, url_info, generate_info):
        if 'page_num' in generate_info.keys():
            page_num = int(generate_info['page_num'])
        else:
            return []

        keyword = quote(url_info['keyword'])
        for page in range(2, page_num + 1):
            new_url = 'https://so.m.jd.com/ware/search._m2wq_list?keyword={keyword}&datatype=1&page={page}&pagesize=100&&sort_type=sort_totalsales15_des'.format(
                keyword=keyword, page=page)
            url_info = {
                'keyword': keyword,
                'url': new_url,
                'page': page
            }

            self.url_queue.put(url_info)


if __name__ == "__main__":
    A = JdSreachSpider(1, 'para_1_1588833220', 'res_10_1589179645')
    A.start()
