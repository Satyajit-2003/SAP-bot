from selenium import webdriver
from time import sleep
import requests
import csv
import os
from config import CONFIG

def send_msg(msg, chat_id):
    #replace every & in msg with %20
    msg = msg.replace("&", "%26")
    requests.get(f"https://api.telegram.org/bot{CONFIG.TELEGRAM_BOT_API}/sendMessage?chat_id={chat_id}&text="+ msg)

def send_details(roll, chat_id):
    msg = ''
    with open(f"attndance_{roll}.csv", "r") as f:
        reader = csv.reader(f)
        msg = ''
        for row in reader:
            msg += f'''
Subject : {row[0]}
Total Classes : {row[1]}
Classes Absent : {row[4]}
Prsent Percentage : {row[2]}

'''
        send_msg(msg, chat_id)

def send_warnings(roll, chat_id):
    with open(f"attndance_{roll}.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if float(row[2]) < 80:
                msg = f'''
WARNING: Your attendance in {row[0]} is {row[2]}
DON'T MISS ANY CLASSES
'''
                send_msg(msg, chat_id)

def extract_data(roll, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CONFIG.GOOGLE_CHROME_BIN
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, executable_path=CONFIG.CHROMEDRIVER_PATH)
    driver.get("https://kiitportal.kiituniversity.net/irj/portal/")

    # Logging in
    driver.find_element(
        "xpath", '//*[@id="logonuidfield"]').send_keys(roll)
    driver.find_element(
        "xpath", '//*[@id="logonpassfield"]').send_keys(password)
    driver.find_element(
        "xpath", '//*[@id="certLogonForm"]/table/tbody/tr[5]/td[2]/input').click()
    sleep(1)

    # Navigating to student self support
    driver.find_element("xpath", '//*[@id="navNodeAnchor_1_1"]').click()
    sleep(3)
    #switching to working area frame
    driver.switch_to.frame(driver.find_element(
        'xpath', '//*[@id="ivuFrm_page0ivu4"]'))
    #going to student self support page
    driver.find_element('xpath', '//*[@class="urLnkDragRelate"]').click()
    sleep(3)

    # finding all the sub menu items
    ele = driver.find_elements(
        'xpath', '//*[@class="urTxtStd"]')
    #clicking student attendance details
    for i in ele:
        if i.text == 'Student Attendance Details':
            i.click()
            break
    sleep(10)

    #switching to working area frame
    driver.switch_to.frame(driver.find_element(
        'xpath', '//*[@id="isolatedWorkArea"]'))

    #It keeps changing to find it again, go to the element, and find the id
    #EG : <input id="WD6A" ....>
    driver.find_element('xpath', '//*[@id="WD52"]').send_keys(CONFIG.SESSION)
    driver.find_element('xpath', '//*[@id="WD6A"]').send_keys(CONFIG.SEMESTER)
    driver.find_element('xpath', '//*[@id="WD77"]').click()

    sleep(8)
    #open csv file attndance.csv and create writer object
    with open(f'attndance_{roll}.csv', 'w', newline='') as csvfile:
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

# if __name__ == "__main__":
#     while 1: 
#         extract_data()
#         send_details()
#         sleep(3600)

