import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from helpers.colors import colors
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
load_dotenv()



def get_ids(links):
    ids=[]
    for i in links:
        for j in reversed(range(0,len(i))):
            if i[j]=='/':
                ids.append(i[j+1:])
                break
    
    return ids


# Create chrome driver
def createDriver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return driver


# make timeout 30 seconds for command find element
def find_element(driver, by, value, timeout=40):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)), f'{colors.red}Timeout while trying to reach an element ❌{colors.reset}')


def main():
    driver=createDriver()
    Handle = os.getenv('CF_HANDEL')
    Password = os.getenv('CF_PASS')
    driver.get('https://codeforces.com/enter?back=%2F%3Ff0a28%3D1')
    find_element(driver,By.XPATH,'//*[@id="handleOrEmail"]').send_keys(Handle)
    find_element(driver,By.XPATH,'//*[@id="password"]').send_keys(Password)
    find_element(driver,By.XPATH,' //*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
    time.sleep(5)
    find_element(driver,By.XPATH,'//*[@id="body"]/div[3]/div[5]/ul/li[5]/a').click()
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/ul/li[3]/a').click()
    links=[]
    for i in range(2,73):
        links.append(find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div[3]/div[1]/div[1]/div[6]/table/tbody/tr[{i}]/td[1]/a[1]').get_attribute('href'))
    
        
    ids=get_ids(links)
    print(ids)

    find_element(driver,By.XPATH,'//*[@id="body"]/div[3]/div[5]/ul/li[7]/a').click()
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[3]/div[6]/table/tbody/tr[2]/td[1]/a').click()
    for i in ids:
        find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[2]/div/a').click()
        find_element(driver,By.XPATH,'//*[@id="contestIdAndName"]').send_keys(i)
        find_element(driver,By.XPATH,'//*[@id="submit"]').click()
        find_element(driver,By.XPATH,'//*[@id="facebox"]/div/div/div/div[2]/div/input[1]').click()


    driver.close()

if __name__ == "__main__":
    main()
