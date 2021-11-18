import os
import time
from math import ceil
from selenium import webdriver

class ResponsiveTester:

    def __init__(self, urls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument('--disable-dev-shm-usage')
        path = "/usr/bin/chromedriver"

        self.browser = webdriver.Chrome(path, chrome_options=chrome_options)
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [320, 360, 480, 960, 1024, 1366, 1920]

    def directory(self, url):
        if not os.path.isdir('screenshots'):
            os.mkdir("screenshots")

        if "www" in url:
            urldir = url[url.index('.')+1:]
        else:
            urldir = url[url.find('//')+1:]

        if ".com" in urldir:
            urldir = urldir[:urldir.index('.com'):]
        else:
            urldir = urldir[:urldir.index('.')]       
        
        if not os.path.isdir(f'screenshots/{urldir}'):
            os.mkdir(f"screenshots/{urldir}")
        
        return urldir

    def screenshot(self, url):
        self.browser.get(url)   
        time.sleep(5)     
        browser_height = self.browser.get_window_size()['height'] 

        urldir = self.directory(url)
        # 윈도우 창 조절
        for size in self.sizes:
            self.browser.set_window_size(size, browser_height)
            # 다시 맨위로 옮긴다.
            self.browser.execute_script("window.scrollTo(0,0)")
            time.sleep(3)
            # return을 붙이면 python code로 값이 온다. 없으면 그대로 실행만함.
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            total_sections = ceil(scroll_size / browser_height)
            for section in range(total_sections):
                # 스크롤을 이동시킨다.
                self.browser.execute_script(f"window.scrollTo(0,{(section+1) * browser_height})")
                # 창 전체를 스크린샷한다.
                self.browser.save_screenshot(f"screenshots/{urldir}/{size}x{section+1}.png")
                time.sleep(2)     

        self.browser.quit()       

    def start(self):
        for url in self.urls:
            self.screenshot(url)
    







