import json

import requests,random,time

from fake_useragent import UserAgent



class KFCSpider:
    def __init__(self):
        self.url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
        self.area = input("请输入查询城市:")
        self.info_list = []
        self.f = open(self.area+'.json','w')

    def headers_get(self):
        return UserAgent().random

    def add_data(self):
        data ={
            "cname": self.area,
            "pid":"",
            "pageIndex": "1",
            "pageSize": "10",
        }
        html_star = requests.post(url=self.url,data=data,headers={'User-Agent':self.headers_get()}).json()
        pageIndex = html_star['Table'][0]['rowcount']
        self.get_data(pageIndex)

    def get_data(self,pageIndex):
        if pageIndex == 10:
            pageIndex = (pageIndex // 10)+1
        else:
            pageIndex = (pageIndex // 10) + 2
        for pageIndex in range(1,pageIndex):

            data = {
                "cname": self.area,
                "pid": "",
                "pageIndex": pageIndex,
                "pageSize": "10",
            }
            html = requests.post(url=self.url,data=data,headers={"User-Agent":self.headers_get()}).json()
            for i in range(0,10):
                item = {}
                item['storeName'] = html['Table1'][i]['storeName']
                item['addressDetail'] = html['Table1'][i]['addressDetail']
                self.info_list.append(item)
                print(item)
            json.dump(self.info_list,self.f,ensure_ascii=False)


    def run(self):
        self.add_data()

if __name__ == '__main__':
    spidr = KFCSpider()
    spidr.run()
