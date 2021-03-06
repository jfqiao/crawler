# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


class XueQiuSearch(object):
    """
    利用36氪搜索得到的文章的结果.
    """

    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 修改userAgent 以及不加载图片
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"  # 设置user-agent请求头
    dcap["phantomjs.page.settings.loadImages"] = False

    search_url = "https://xueqiu.com/k?q={}#/timeline"

    kr_url = "http://xueqiu.com"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = XueQiuSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            driver = webdriver.PhantomJS(
                executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                desired_capabilities=XueQiuSearch.dcap)
            driver.set_page_load_timeout(30)
            driver.get(url)
            # time.sleep(0.5)   # 等待加载数据,这个不一定是0.5s,需要调整,调整的方案是等待加载好了,但是设置好了不知道为什么没有起作用
            driver.implicitly_wait(10)
            logging.info("Get %s success." % url)
            page_cnt = driver.page_source
            while len(url) > 0 and failure < 10:
                if page_cnt:
                    bs_obj = BeautifulSoup(page_cnt, "html.parser")
                    result_links = bs_obj.findAll("article", class_="timeline__item")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(XueQiuSearch.item)
                            title_node = result.find("div", class_="timeline__item__content timeline__item__content--longtext")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("h3").get_text()
                            item_ins['abstract'] = result.find("div", class_="content content--description").get_text()
                            item_ins['date'] = result.find("a", class_="date-and-source").get_text().split(" ")[0]
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse 36kr result error. ErrorMsg: %s" % str(e))
                max_page -= 1
                if max_page <= 0:
                    break
                js = "document.body.scrollTop=1000"
                driver.execute_script(js)
                driver.refresh()
                time.sleep(0.5)
                page_cnt = driver.page_source
        except BaseException as e:
            logging.error("Get 36Kr search result error. ErrorMsg: %s" % str(e))
        finally:
            driver.quit()
        return result_list


if __name__ == "__main__":
    url_list = XueQiuSearch.search("区块链", search_page=1)    # 已经测试过了,运行正常
    print(url_list["result_list"])
