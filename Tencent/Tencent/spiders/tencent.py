# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "https://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class ='even'] | //tr[@class ='odd']")
        for node in node_list:
            item = TencentItem()
            item['positionName'] = node.xpath("./td[1]//text()").extract()[0]
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]
            try:
                item['positionType'] = node.xpath("./td[2]//text()").extract()[0]
            except:
                item['positionType'] = ''
            item['peopleNumber'] = node.xpath("./td[3]//text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]//text()").extract()[0]
            item['publicTime'] = node.xpath("./td[5]//text()").extract()[0]
            yield item

        # if self.offset < 3110:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)

        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url, callback=self.parse)
