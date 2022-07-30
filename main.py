from httplib2 import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
from time import sleep
import requests
import csv
import os

def extract_password():
    with open("pass.pkl", "rb") as f:
        dc = pickle.load(f)
    return dc

def send_msg(msg):
    requests.get("https://api.telegram.org/bot1926784886:AAGY021L84s55x3aVgMk2EgSTfp2JIJ3Hlg/sendMessage?chat_id=1124005171&text="+ msg)

def send_details():
    msg = ''
    with open("attndance.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            msg += f'''
Subject : {row[0]}
Total Classes : {row[1]}
Classes Present : {row[7]}
Classes Absent : {row[3]}
Prsent Percentage : {row[2]}
Faculty : {row[6]}

'''
    send_msg(msg)

chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome( chrome_options=chrome_options) #, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
driver.get("https://kiitportal.kiituniversity.net/irj/portal/")

Credentials = extract_password()
# Logging in
driver.find_element(
    "xpath", '//*[@id="logonuidfield"]').send_keys(Credentials[0])
driver.find_element(
    "xpath", '//*[@id="logonpassfield"]').send_keys(Credentials[1])
driver.find_element(
    "xpath", '//*[@id="certLogonForm"]/table/tbody/tr[5]/td[2]/input').click()
sleep(1)

# Navigating to student self support
driver.find_element("xpath", '//*[@id="navNodeAnchor_1_1"]').click()
sleep(3)
driver.switch_to.frame(driver.find_element(
    'xpath', '//*[@id="ivuFrm_page0ivu3"]'))

driver.find_element('xpath', '//*[@class="urLnkDragRelate"]').click()
sleep(3)

ele = driver.find_elements(
    'xpath', '//*[@class="urTxtStd"]')
#document.querySelector("#Link4c1d4655").scrollIntoView()

for i in ele:
    if i.text == 'Student Attendance Details':
        i.click()
        break
sleep(5)

driver.switch_to.frame(driver.find_element(
    'xpath', '//*[@id="isolatedWorkArea"]'))
driver.find_element('xpath', '//*[@id="WD5C"]').send_keys("2022-2023")
driver.find_element('xpath', '//*[@id="WD74"]').send_keys("Autumn")
driver.find_element('xpath', '//*[@id="WD81"]').click()

sleep(4)
#open csv file attndance.csv and create writer object
with open('attndance.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    var = 2
    while 1:
        try:
            details_list = []
            for i in range(2,11):
                details_list.append(driver.find_element('xpath', f'/html/body/table/tbody/tr/td/div/div[1]/span/span[3]/div/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[{var}]/td[{i}]/span/span').text)
            writer.writerow(details_list)
            print(details_list)
        except:
            break    
        var  = var +1

driver.quit()

send_details()

