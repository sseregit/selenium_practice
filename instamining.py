import time
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class Instamining:

    def __init__(self, hashtag, id, pw):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument('--disable-dev-shm-usage')
        path = "/usr/bin/chromedriver"

        self.browser  = webdriver.Chrome(path,chrome_options=chrome_options)
        self.id = id
        self.pw = pw
        self.hashtag = hashtag

    def wait_for(self, locator):
        return WebDriverWait(self.browser,15).until(EC.presence_of_element_located(locator))



    def login(self):
        while True:
            count = 0 
            try:       
                count += 1                
                login_inputs = self.browser.find_elements_by_class_name("_2hvTZ")
                login_button = self.browser.find_element_by_class_name("L3NKy")

                login_inputs[0].send_keys(self.id)
                login_inputs[1].send_keys(self.pw)            
                login_button.click()                            
                time.sleep(5)
                break                    
            except TimeoutException:
                self.browser.refresh()
                time.sleep(5)
                continue
            except NoSuchElementException:
                self.browser.quit() 

    def file(self, result):
        file = open(f"{self.hashtag}_result.csv","w")
        writer = csv.writer(file)
        writer.writerow(["Hashtags","Posts"])
        for re in result:
            writer.writerow(re)          

    def dataminung(self):
        self.browser.get(f"https://www.instagram.com/")
        time.sleep(5)

        self.login()
        time.sleep(10)
        search_input = self.wait_for((By.CLASS_NAME,'XTCLo'))

        search_input.send_keys(f'#{self.hashtag}')

        search = self.wait_for((By.CLASS_NAME,'fuqBx'))

        time.sleep(5)

        hashtags = search.find_elements_by_class_name('qyrsm')
        counting = search.find_elements_by_class_name('_0PwGv')

        if hashtags:
            length = range(len(hashtags))

            result = []

            for i in length:
                result.append((hashtags[i].text,counting[i].text))
            
            self.file(result)

        self.browser.quit()        
