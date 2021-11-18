import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class GoogleKeywordScreenshooter:

    def __init__(self, keyword, screenshots_dir, max_pages = 1):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument('--disable-dev-shm-usage')
        path = "/usr/bin/chromedriver"
        self.browser = webdriver.Chrome(path, chrome_options=chrome_options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_pages = max_pages
    
    def start(self):
        try:
            os.mkdir(self.screenshots_dir)
        except FileExistsError:
            pass
        self.browser.get("https://google.com")
        # className 찾기
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        # input의 key넣기 send_keys는 input이 아니면 에러가남!
        search_bar.send_keys(self.keyword)
        # input Enter값 보내기
        search_bar.send_keys(Keys.ENTER)
        
        while True:
            page = self.browser.find_element_by_class_name("YyVfkd").text
                    # WebDriverWait 10초동안 대기 시킴
            # until(EC.presence_of_all_elements_located((By.CLASS_NAME, "class_name")))
            # element의 위치가 생길 때 까지
            try:
                shitty_element = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ULSxyf")))
                # 필요없는 요소를 삭제함 JS코드를 보냄.
                self.browser.execute_script("""
                const shitty = arguments[0];
                shitty.parentElement.removeChild(shitty)
                """,shitty_element[0])
            except Exception:
                pass        
            # classname안에 classname찾기
            search_results = self.browser.find_element_by_id("rso").find_elements_by_class_name("g")
            # tag를 찾아서 print하기
            for index,search_result in enumerate(search_results):
                # class만 가져옴.
                class_name = search_result.get_attribute("class")
                if "g" in class_name:
                    search_result.screenshot(f"{self.screenshots_dir}/p{page}k{self.keyword}x{index}.png")

            if self.max_pages == int(page):
                break

            next_button = self.browser.find_element_by_id("pnnext")
            next_button.click()
            # 시간주기
            time.sleep(2)
            
                                                                        
    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots", 3)        
domain_competitors.start()
domain_competitors.finish()
