# encoding=utf-8
import pymssql
import random
import time

import requests
from lxml import etree
from fake_useragent import UserAgent


class Scatter(object):
    def __init__(self, kw, site):
        self.kw = kw
        self.site = site
        self.proxy_host = "47.103.103.44"
        self.proxy_user = "sa"
        self.proxy_pwd = "jerryAa0902aA"
        self.proxy_db = "AmazonRankDB"
        self.selector = None

        self.asin_host = "47.52.156.201"
        self.asin_user = "py"
        self.asin_pwd = "jerryAa0902aA"
        self.asin_db = "MC_FrameworkBase"

    def get_url(self):
        """根据关键词和站点拼接url"""
        if self.site == "us":
            url_detail = "https://www.amazon.com/s?k="
        elif self.site == "uk":
            url_detail = "https://www.amazon.co.uk/s?k="
        elif self.site == "jp":
            url_detail = "https://www.amazon.co.jp/s?k="
        elif self.site == "de":
            url_detail = "https://www.amazon.de/s?k="
        elif self.site == "fr":
            url_detail = "https://www.amazon.fr/s?k="
        elif self.site == "it":
            url_detail = "https://www.amazon.it/s?k="
        elif self.site == "ca":
            url_detail = "https://www.amazon.ca/s?k="
        elif self.site == "es":
            url_detail = "https://www.amazon.es/s?k="
        elif self.site == "mx":
            url_detail = "https://www.amazon.com.mx/s?k="
        elif self.site == "au":
            url_detail = "https://www.amazon.com.au/s?k="
        else:
            url_detail = None

        keyword_list = self.kw.split(' ')
        keyword_num = len(keyword_list)
        current_num = 0
        while current_num < keyword_num:
            url_detail += keyword_list[current_num] + "+"
            current_num += 1
        return url_detail

    def get_ua_random(self):
        """获取随机ua"""
        user_agent = UserAgent()
        ua = user_agent.random
        print(ua)
        return ua

    def get_proxy_random(self):
        """获取代理ip"""
        conn = pymssql.connect(host=self.proxy_host, user=self.proxy_user, password=self.proxy_pwd,
                               database=self.proxy_db)
        cursor = conn.cursor()
        sql = "select ProxyIp from Table_Proxy"
        cursor.execute(sql)
        proxy_ip_list = cursor.fetchall()
        proxy_ip = proxy_ip_list[random.randint(0, len(proxy_ip_list) - 1)]
        cursor.close()
        conn.close()

        return proxy_ip[0]

    def get_rank(self):
        """根据关键词抓取页面"""
        proxies = {"http": "http://" + self.get_proxy_random(), }
        headers = {
            "User-Agent": self.get_ua_random(),
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Cookie": "session-id=132-8802206-0435751; ubid-main=135-0767665-7187105; session-id-time=2082787201l; session-id-jp=357-1717233-7335745; ubid-acbjp=357-1663697-6823234; session-id-time-jp=2198200390l; s_pers=%20s_dl%3D1%7C1567482190446%3B%20gpv_page%3DUS%253ASC%253A%2520SellerCentralLogin%7C1567482190456%3B%20s_ev15%3D%255B%255B%2527www.baidu.com%2527%252C%25271567480390459%2527%255D%255D%7C1725333190459%3B; UM_distinctid=16d3ccb17bb124-0557dcd2b36b26-3c375c0f-144000-16d3ccb17bc152; s_vnum=2001316394530%26vn%3D8; s_fid=1D14AD2F7EC9D0A6-2BFE0FE22F03F8FC; regStatus=pre-register; x-wl-uid=1rXknQS2QRFXHKSTrf0Yf7VSu8IECLiW+Z5GtyWgOZC08rwSz7chCALDM4DvfAI83W490s9ELm6ptEELQDaH+gOBQGUyOcfeP19xiulg0K19sxX0OH9Wrq4tN++OkqERdZul4BiVXGmU=; sst-main=Sst1|PQFDNrpVnAIMJcprCh3FRctvC_sNZ-dnONDRXNnyywkvD83UdoSSZ6fcgdqHQKIsgqyaIM9PlwLzLtDZzfvniK5p-VHLLLTHFZS90TPZ4zlBfvt1DeddbZT1seRV23MG68t8mjdgBcGWulxUxi7e-4viacRjlbzu_z-GWmKHDce4e8ZNXZBEq8iS2TkM8lSUN9fFeX7nCJ76KHEoM0UvC1CXTHMXOExi36j8_cpo6jCXMZAhyycNLH0I4jKS_Vc_LnL_YBYnYXfS1IRk3gqgIJVcnQdw8Em46Q2msHX_OAIAmtAUT-_axQHN6L2Nm4xj5Y8Xzo-4UDaNo4ISj6Oh6C7naA; i18n-prefs=USD; amznacsleftnav-8b1cbb0f-3455-4731-bd98-3e8937ea257b=1; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws-target-static-id=1578016209581-504291; aws-target-data=%7B%22support%22%3A%221%22%7D; s_vn=1606795321258%26vn%3D2; aws-target-visitor-id=1578016209585-359836.22_21; s_dslv=1578016210978; s_nr=1578016210984-Repeat; session-token=8qNqGsHADeunIFw8sG1fgKibtKwxZrjZ67zIqJ5jjBpjDQ2Hv8H79KhL/j8eHnK5NJdkDX9LTu9A1PWUlBMEOILJn/y0hnQn8vDYiWHEcDClwuE8jpAOK5Y0Qzx3REmPcugejcpf6Ik5NoTqaz6+21274/MruqvM38rKX0ojbNSTShbvLqDLjMZDaS2jsgzZ; csm-hit=tb:TVYDW8190QX1M3JFTS7Y+s-5CRSKW1N6X5TZ7DKX3J1|1578967789890&t:1578967789890&adb:adblk_no",
            'Referer': "https://www.amazon.com/s?k=office%20chair&qid=1578901743&ref=glow_cls&refresh=1"
        }
        url_detail = self.get_url()
        try:
            response = requests.get(url_detail, headers=headers, proxies=proxies, timeout=2)
            print("页面爬取成功")
        except:
            print("页面爬取失败")
            return None
        list_html = response.text
        return list_html

    def get_robot(self):
        """判断是否进入验证码界面"""
        robot = self.selector.xpath("//h4[text()='Enter the characters you see below']")
        if robot:
            print("Enter the verification code page")
            return True
        else:
            return False

    def parse_html(self):
        # 提取数据，获取相应asin所对应的排名
        html = self.get_rank()
        try:
            self.selector = etree.HTML(html)
        except:
            print("can only parse strings")
            return None

        if self.get_robot():
            return None

        asin_list = self.selector.xpath("//div[@class='s-result-list s-search-results sg-row']/div/@data-asin")

        sponsored_list = self.selector.xpath(
            "//div[@class='s-result-list s-search-results sg-row']//div[contains(@class,'a-row a-spacing-micro')]/ancestor::div/@data-asin")
        for sponsored in sponsored_list:
            asin_list.remove(sponsored)

        delivery_area = self.selector.xpath('//span[@id="glow-ingress-line2"]/text()')
        # print("配送地址:%s" % delivery_area)
        # 去除列表中的空字符串
        asin_list = list(filter(None, asin_list))

        return asin_list

    def get_connect(self, host, user, pwd, dbname):
        """获取数据库连接"""
        while True:
            print('start connect db')
            try:
                db = pymssql.connect(host, user, pwd, dbname)
                print('Database connection succeeded')
                return db
            except Exception as e:
                print(e)
                print('Database connection failed, wait 300s continue')
                time.sleep(300)
                continue

    def get_asin(self):
        """从数据库中获取数据:asin"""
        db = self.get_connect(self.asin_host, self.asin_user, self.asin_pwd, self.asin_db)
        cursor = db.cursor()
        sql = "select ASIN from dbo.FlowFBALog"
        # sql = "select ASIN from dbo.FlowFBALog where ASIN='B07PPFCZCG'"
        try:
            cursor.execute(sql)
        except:
            print("---Database query failed---")
        self.asin_list = cursor.fetchall()
        # mylog.info(self.asin_list)
        cursor.close()
        db.close()
        self.asin_disdinct()

        return self.new_asin_list

    def asin_disdinct(self):
        """将从数据库中获取的asin列表去重"""
        self.new_asin_list = list(set(self.asin_list))

    def create_scatter_data(self):
        """创建散点图需要的列表数据"""
        asin_list = self.parse_html()
        if asin_list is None:
            return
        our_asin_list = self.get_asin()
        scatter_list = list()
        for i in range(int(len(asin_list)/4)):
            for j in range(1,5):
                scatter_list.append([j,int(len(asin_list)/4) - i])

        k = 0

        for l2 in scatter_list:
            l3 = []
            l3.append(asin_list[k])
            if tuple(l3) in our_asin_list:
                l2.append(1)
            else:
                l2.append(0)

            l2.append(asin_list[k])

            k += 1

        return scatter_list


if __name__ == '__main__':
    s = Scatter("office chair", "us")
    l1 = s.create_scatter_data()
    print(l1)
