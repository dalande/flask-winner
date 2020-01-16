# encoding=utf-8
# encoding:utf-8
from selenium import webdriver
import time
import logging
import getpass
import sys


class MyLog(object):
    # 类MyLog的构造函数
    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)

        self.logFile = sys.argv[0][0:-3] + '.log'  # print(sys.argv[0])   代表文件名 输出 mylog.py
        self.formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s\r\n')

        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)

        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)

        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


class ProfileComment(object):
    def __init__(self):
        self.link_list = list()
        self.new_link_list = list()
        self.link = None
        self.current_time = self.get_current_time()
        self.current_day = None
        self.author_info_dict = dict()
        self.author_tuple = None


    @staticmethod
    def get_browser():
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.migration.version', 9001)
        profile.set_preference('permissions.default.image', 2)
        browser = webdriver.Firefox(profile, executable_path="/usr/local/sbin/geckodriver")
        return browser

    @staticmethod
    def get_current_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @staticmethod
    def get_current_day():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).split(' ')[0]

    def get_star_ave(self, star_list):
        """平均星级"""
        star_sum = 0
        for star in star_list:
            star_sum += int(star)
        return round(star_sum / len(star_list), 2)

    def get_bad_num(self, star_list):
        """差评数"""
        bad_num = 0
        for star in star_list:
            if int(star) <= 3:
                bad_num += 1
        return bad_num

    def get_review_num_m(self, date_list):
        """获取近一月,一年评论数"""
        review_num_y = 0
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0
        m5 = 0
        m6 = 0
        m7 = 0
        m8 = 0
        m9 = 0
        m10 = 0
        m11 = 0
        mylog.info(date_list)
        for date in date_list:
            standard_date = self.t1_to_timestamp(' '.join(date.split(' ')[-3:]))
            current_timestamp = self.t2_to_timestamp(self.current_time)
            if current_timestamp - standard_date < 31536000:
                review_num_y += 1
            if current_timestamp - standard_date < 2505600:
                m1 += 1
            if current_timestamp - standard_date < 5011200:
                m2 += 1
            if current_timestamp - standard_date < 7516800:
                m3 += 1
            if current_timestamp - standard_date < 10022400:
                m4 += 1
            if current_timestamp - standard_date < 12528000:
                m5 += 1
            if current_timestamp - standard_date < 15033600:
                m6 += 1
            if current_timestamp - standard_date < 17539200:
                m7 += 1
            if current_timestamp - standard_date < 20044800:
                m8 += 1
            if current_timestamp - standard_date < 22550400:
                m9 += 1
            if current_timestamp - standard_date < 25056000:
                m10 += 1
            if current_timestamp - standard_date < 27561600:
                m11 += 1
        m_dict = [m1,m2-m1,m3-m2,m4-m3,m5-m4,m6-m5,m7-m6,m8-m7,m9-m8,m10-m9,m11-m10,review_num_y-m11]
        return m1, review_num_y, m_dict

    def t1_to_timestamp(self, review_date):
        """将Dec 14, 2019格式的时间转换为时间戳"""
        str1 = time.strptime(review_date, '%b %d, %Y')
        timestamp = int(time.mktime(str1))
        return timestamp

    def t2_to_timestamp(self, recent_time):
        """将2013-10-10 23:40:00格式的时间转换为时间戳"""
        recent_date = recent_time.split(' ')[0]
        timeArray = time.strptime(recent_date, "%Y-%m-%d")
        timestamp2 = int(time.mktime(timeArray))
        return timestamp2

    def get_profile_html(self, url):
        """爬取profile页面"""
        mylog.info("current profile url:{}".format(url))
        self.author_info_dict = dict()
        self.current_time = self.get_current_time()

        browser = self.get_browser()
        try:
            browser.get(url)
        except Exception as e:
            mylog.info(e)
            browser.close()
            return
        time.sleep(3)

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

        try:
            share = browser.find_elements_by_xpath("//span[contains(text(),'no activity to share.')]")
            if share:
                mylog.info("no activity to share.")
                browser.close()
                return "no activity to share."
        except:
            pass

        while True:
            try:
                es = browser.find_element_by_css_selector("#profile-at-feed-footer")
                mylog.info('Page loading is not complete, wait 5s...')
                time.sleep(5)
            except:
                mylog.info('Page loaded...')
                break
        try:
            author = browser.find_element_by_xpath('//div[@id="customer-profile-name-header"]/descendant::span')
        except Exception as e:
            mylog.error(e)
            browser.close()
            return "Query failed"


        try:
            about = browser.find_element_by_xpath("//span[contains(@class,'read-more-text')]")
        except:
            about = None

        try:
            rank = browser.find_element_by_xpath('//div[@class="a-row"]/span')
        except:
            rank = None

        # 平均星级和留差评数,星级等于或者低于三星是差评
        star_elem_list = browser.find_elements_by_xpath(
            "//div[@class='a-row']/descendant::i[contains(@class,'review')]/span")
        star_list = list()
        for stat_elem in star_elem_list:
            star_list.append(stat_elem.get_attribute("innerText").split(' ')[0])
        star_ave = self.get_star_ave(star_list)
        bad_num = self.get_bad_num(star_list)

        # 评论日期列表
        date_elem_list = browser.find_elements_by_xpath("//span[contains(text(),'reviewed a product')]")
        date_list = list()
        for date_elem in date_elem_list:
            date_list.append(date_elem.text)

        review_num_m, review_num_y, m_dict = self.get_review_num_m(date_list)

        insights_elem_list = browser.find_elements_by_xpath(
            '//div[contains(@class,"dashboard-desktop-stat-value")]/descendant::span')
        author_info_list = list()
        for insights_elem in insights_elem_list:
            author_info_list.append(insights_elem.text)
        self.author_info_dict["profile_url"] = url
        self.author_info_dict["author"] = author.text
        self.author_info_dict["about"] = about.text if about else None
        self.author_info_dict["reviewer_ranking"] = rank.text[1:] if rank else 0
        self.author_info_dict["helpful_votes"] = author_info_list[0]
        self.author_info_dict["review_num"] = author_info_list[1]
        self.author_info_dict["month_num"] = review_num_m
        self.author_info_dict["year_num"] = review_num_y
        self.author_info_dict["m_dict"] = m_dict
        self.author_info_dict["bad_num"] = bad_num
        self.author_info_dict["star_ave"] = star_ave
        self.author_info_dict['current_time'] = self.current_time

        self.author_tuple = self.dictValueToTuple(self.author_info_dict)
        # self.save_prime_data()
        # print(self.author_info_dict)

        browser.close()

        return self.author_info_dict

    def dictValueToTuple(self, sigle_review_dict):
        """将评论者信息字典的值转化为元组"""
        author_list = list()
        for v in sigle_review_dict.values():
            author_list.append(v)
        author_tuple = tuple(author_list)
        return author_tuple


mylog = MyLog()


def browser_start(account):
    p = ProfileComment()
    url = 'https://www.amazon.com/gp/profile/amzn1.account.{}/ref=cm_cr_dp_d_gw_tr?ie=UTF8'.format(account)

    data = p.get_profile_html(url)
    mylog.info('--------------sleep 1800s------------')
    return data
