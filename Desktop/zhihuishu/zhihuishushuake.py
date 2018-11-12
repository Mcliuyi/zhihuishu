# -*- coding:utf-8 -*-
# Author: liuyi
# email: ly288@qq.com
# python:3.6

from selenium import webdriver
import time


class Zhihuishu(object):

    def __init__(self, url):
        # 账号密码
        self.url = url
        self.web = webdriver.Chrome()
        self.web.get(self.url)

    def login(self, user, pwd):
        """
        登錄
        :param user: 用戶名
        :param pwd: 密碼
        :return:
        """

        self.wait()
        school = self.web.find_element_by_id("clSchoolId")
        # self.web.execute_script("arguments[0].value = '2245';", school)
        self.web.find_element_by_id("clCode").clear()
        self.web.find_element_by_id("clCode").send_keys(user)
        self.web.find_element_by_id("clPassword").clear()
        self.web.find_element_by_id("clPassword").send_keys(pwd)

        self.web.find_element_by_class_name("wall-sub-btn").click()
        self.web.find_element_by_id("quickSearch").send_keys("吉首大学")
        self.web.execute_script("arguments[0].value = '2245';", school)
        self.web.find_element_by_class_name("wall-sub-btn").click()
        url = self.web.current_url

    def learn(self):
        """
        進入課程
        :return:
        """
        self.wait()
        # 切換頁面
        # 獲取正在學校的課程的第一個
        try:
            #獲取學習進度
            p = self.web.find_elements_by_css_selector("span.mySchedulePrice")
            print(p[-1].value_of_css_property("left"))
            curricula = self.web.find_elements_by_link_text("继续学习")
            for i in range(len(p)):
                if i >= 2:
                    self.web.find_element_by_id("course_recruit_studying_next").click()
                    time.sleep(2)
                    curricula.clear()
                    curricula = self.web.find_elements_by_link_text("继续学习")
                    prog = p[i].value_of_css_property("left")
                    pp = int(prog[:-3])
                else:
                    prog = p[i].text
                    pp = int(prog[-5:-3])
                print(pp)

                if pp >= 82:
                    continue
                else:
                    if i>=2:
                        curricula[i-2].click()
                    else:
                        curricula[i].click()

        except BaseException as e:
            self.web.find_element_by_partial_link_text("开始学习").click()
        # 获取打开的多个窗口句柄
        windows = self.web.window_handles
        # 切换到当前最新打开的窗口
        self.web.switch_to.window(windows[-1])

    def offtis(self):
        """
        關閉提示
        :return:
        """

        self.wait()
        try:
            # 確定提示
            self.web.find_element_by_class_name("popbtn_yes").click()
            # 我已知曉
            # self.web.find_element_by_xpath('//*[@id="j-assess-criteria_popup"]/div[9]/div/a').click()
            # //*[@id="j-assess-criteria_popup"]/div[9]/div/a
        except BaseException as e:
            pass
        time.sleep(3)
        try:
            self.web.find_element_by_css_selector('div.knowbtn_box>a').click()
        except BaseException as e:
            print(e)

    def play(self):
        """播放視頻:return:"""

        while True:
            self.wait()
            o = self.web.find_element_by_css_selector("div.passTime")
            l = o.value_of_css_property('width')
            print(l)
            if l == "100%":
                try:
                    self.web.find_element_by_partial_link_text("下一节").click()
                    time.sleep(10)
                except BaseException:
                    self.web.close()
                    # 获取打开的多个窗口句柄
                    windows = self.web.window_handles
                    # 切换到当前最新打开的窗口
                    self.web.switch_to.window(windows[-1])
                    self.learn()
                    self.offtis()


            else:
                time.sleep(10)
                try:
                    self.web.find_element_by_css_selector("div#popbox_overlay")
                    # 判斷是否出現題目
                    self.web.find_element_by_css_selector("a.popbtn_cancel").click()
                except BaseException as e:
                    print(e)
                    continue

    def wait(self):
        self.web.implicitly_wait(30)


def main():
    url = "https://passport.zhihuishu.com/login?service=http://online.zhihuishu.com/onlineSchool/#studentID"
    user = input("请输入你的学号后三位：")
    pwd = input("请输入你的密碼： ")
    user = "2017402" + user

    zhihuishu = Zhihuishu(url)

    zhihuishu.login(user, pwd)

    zhihuishu.learn()
    zhihuishu.offtis()
    time.sleep(3)
    zhihuishu.play()


if __name__ == "__main__":
    main()