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


def write_fin(links, file):
    for i, j in links.items():
        file.write(i+j+'\n')


def read_file(file):
    links = {}
    link = list(file.read().strip().split('\n'))
    for i in range(len(link)):
        if link[i][-1:] == "\t":
            link[i] = link[i][0:-1]
    for i in link:
        links[i[:-1]] = i[-1]
    return links


# Create chrome driver
def createDriver():
    chrome_options = webdriver.ChromeOptions()
   # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return driver


# make timeout 30 seconds for command find element
def find_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)), f'{colors.red}Timeout while trying to reach an element ❌{colors.reset}')

#get the ids of contests
def get_ids(links):
    ids=[]
    for i in links:
        for j in reversed(range(0,len(i))):
            if i[j]=='/':
                ids.append(i[j+1:])
                break
    
    return ids
            
# check if the element exict or not     
def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    except InvalidSelectorException:
        return False
    return True


def make_contest(driver,contest_num,links):
    contest_name=f'contest {contest_num}'
    Handle = os.getenv('CF_HANDEL')
    Password = os.getenv('CF_PASS')
    driver.get('https://codeforces.com/enter?back=%2F')
    ids=get_ids(links)
    find_element(driver,By.XPATH,'//*[@id="handleOrEmail"]').send_keys(Handle)
    find_element(driver,By.XPATH,'//*[@id="password"]').send_keys(Password)
    find_element(driver,By.XPATH,' //*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
   
    time.sleep(3)
    find_element(driver,By.XPATH,'//*[@id="body"]/div[3]/div[5]/ul/li[5]/a').click()
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/ul/li[3]/a').click()
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[2]/div/a').click()
    find_element(driver,By.XPATH,'//*[@id="contestName"]').send_keys(contest_name)
    find_element(driver,By.XPATH,'//*[@id="contestDuration"]').send_keys('120')
    x='A'
    first=1
    row=1
    no_problem=0 
    for i in ids:
        for j in range(0,3):
            problem=i+x
            if first:
                find_element(driver,By.XPATH,'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr/td[2]/form/label/input').send_keys(problem)
                time.sleep(2)
                find_element(driver,By.XPATH,'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr/td[1]').click()
                time.sleep(2)
                first=0
            else:
                find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[2]/form/label/input').send_keys(problem)
                time.sleep(2)
                find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[1]').click()
                time.sleep(2)
                if  check_exists_by_xpath(f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[2]/form/div/span[1]',driver) :
                    no_problem=1
                    problem+='1'
                    find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[2]/form/label/input').clear()
                    find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[2]/form/label/input').send_keys(problem)
                    time.sleep(2)
                    find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div/div[2]/div[6]/table/tbody/tr[{str(row)}]/td[1]').click()
                    time.sleep(2)

            row+=1
            if no_problem :
                no_problem=0
                x='c2'
            else :
                x=chr(ord(x)+1)
        x='A'

    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div/form[2]/input[2]').click()
    time.sleep(5)

def main():
    file = open('final_links.txt', 'r')
    links=read_file(file)
    file.close()
    driver=createDriver()

    contest_num=int(links['contest_number'])
    links['contest_number']=str(contest_num+1)
    linky=[]

    for i,j in links.items():
        if j=='0':
            linky.append(i)
            links[i]='1'
        if len(linky)==2:
           break
    
    make_contest(driver=driver,contest_num=contest_num,links=linky)

    #write the file after changing the values of each link
    file = open('script/final_links.txt', 'w')
    write_fin(links, file)
    file.close()




if __name__ == "__main__":
    main()

