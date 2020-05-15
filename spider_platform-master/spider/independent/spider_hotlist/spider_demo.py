from spider.independent.spider_hotlist.hotlist_spider import SeleniumjdSpider


if __name__ == "__main__":
    # 京东商品排行榜爬虫
    spider = SeleniumjdSpider(3, 'para_3_1589353153', 'res_19_1589353228')
    spider.start()
