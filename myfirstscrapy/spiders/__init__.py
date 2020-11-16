# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import time
import re

class SimplifiedSpider(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        urls = [
            # 'https://blog.scrapinghub.com',
            # 'http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22fld%22%3A%22dataTime.start%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%222012-11-01%22%7D%2C%7B%22fld%22%3A%22dataTime.end%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%222020-09-30%22%7D%2C%7B%22fld%22%3A%22pageNum%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%221%22%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22ASC%22%7D%5D%7D&tr=A&ss=1&pageNo=1&pageSize=500'
            #'http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22fld%22%3A%22dataTime.start%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%221946-05-15%22%7D%2C%7B%22fld%22%3A%22dataTime.end%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%222020-10-04%22%7D%2C%7B%22fld%22%3A%22pageNum%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%221%22%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22ASC%22%7D%5D%7D&tr=A&ss=1&pageNo=1&pageSize=500'
            'http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22fld%22%3A%22dataTime.start%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%221989-01-01%22%7D%2C%7B%22fld%22%3A%22dataTime.end%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%222020-11-16%22%7D%2C%7B%22fld%22%3A%22pageNum%22%2C%22cdr%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%221%22%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&ss=1&pageNo=1&pageSize=500'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for post in response.css('div.post-item'):
        for post in response.css('div.sreach_li'):
            dstring = post.css('div.listinfo::text').get().strip('\n\t')
            tsstring = self.parsetime(dstring)
            yield {
                'date': tsstring,         
                'location': dstring,       
                'tags': post.css('div.incon_text div.keywords a::text').getall(),
                'title': post.css('h3 a.open_detail_link::text').get(),
                'content': post.css('div.incon_text p::text').get().strip('\n\t'),
                'id': str(time.time())
                }

        next_page = self.getnextpage(response.url)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parsetime(self, text):
        ret = re.search(r'(\d+)年(\d+)月(\d+)日', text).groups()

        if len(ret) != 3:
             return text

        return '%s/%s/%s' % (ret[1], ret[2], ret[0])


    def getnextpage(self, urlstr):   
        substr = [ss for ss in urlstr.split('&') if 'pageNo' in ss]
        print('-------------->   %s' % substr)
        substr = substr[0] if len(substr) > 0 else None

        if substr is None:
            return None

        sss = substr.split('=')
        if sss[1] is None:
            return None
        
        newsubstr = 'pageNo=' + str(int(sss[1]) + 1)

        # if int(sss[1]) > 3: return None

        return urlstr.replace(substr, newsubstr)