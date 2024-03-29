from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep, ctime
import requests
import csv
import os
from config import CONFIG

def send_msg(msg, chat_id):
    #replace every & in msg with %26
    msg = msg.replace("&", "%26")
    requests.get(f"https://api.telegram.org/bot{CONFIG.TELEGRAM_BOT_API}/sendMessage?chat_id={chat_id}&text="+ msg)

def send_details(roll, chat_id):
    msg = ''
    with open(f"attndance_{roll}.csv", "r") as f:
        reader = csv.reader(f)
        head_found = False
        msg = ''
        for row in reader:
            if (not head_found):
                sub_row = row.index("Subject")
                total_class_row = row.index("Total No. of Days")
                class_absent_row = row.index("No.of Absent")
                pres_perc_row = row.index("Total Percentage")
                absent_affordable_row = row.index('Absents affordable')
                msg += f'Updation time: {row[-1]}\n\n'
                head_found = True
                continue

            msg += f'''
Subject : {row[sub_row]}
Total Classes : {row[total_class_row]}
Classes Absent : {row[class_absent_row]}
Prsent Percentage : {row[pres_perc_row]}
Absents Affordable : {row[absent_affordable_row]}

'''
        send_msg(msg, chat_id)

def send_warnings(roll, chat_id):
    with open(f"attndance_{roll}.csv", "r") as f:
        reader = csv.reader(f)
        head_found = False
        for row in reader:
            if (not head_found):
                sub_row = row.index("Subject")
                pres_perc_row = row.index("Total Percentage")
                absent_affordable_row = row.index('Absents affordable')
                head_found = True
                continue
            if float(row[pres_perc_row]) < 80:
                if int(row[absent_affordable_row]) > 0:
                    msg = f'''
WARNING: Your attendance in {row[sub_row]} is {row[pres_perc_row]}
{row[absent_affordable_row]} ABSENTS CAN BE AFFORDED
'''
                else:
                    msg = f'''
WARNING: Your attendance in {row[sub_row]} is {row[pres_perc_row]}
NO ABSENTS CAN BE AFFORDED
'''
                send_msg(msg, chat_id)

def extract_data(roll, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CONFIG.GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, executable_path=CONFIG.CHROMEDRIVER_PATH)

    tries = 0
    while tries < 10:
        try:
            # trying Logging in
            driver.get("https://kiitportal.kiituniversity.net/irj/portal/")
            driver.find_element(
                "xpath", '//*[@id="logonuidfield"]').send_keys(roll)
            driver.find_element(
                "xpath", '//*[@id="logonpassfield"]').send_keys(password)
            driver.find_element(
                "xpath", '//*[@id="certLogonForm"]/table/tbody/tr[5]/td[2]/input').click()
            break
        except:
            if tries == 9:
                print(f"Login attempt failed for {roll} at time {ctime()}")
                return
            tries += 1
            sleep(30)
            continue
    sleep(1)

    # Navigating to student self support
    try:
        driver.find_element("xpath", '//*[@id="navNodeAnchor_1_1"]').click()
    except:
        pass
    sleep(3)
    #switching to working area frame
    #This keeps changing between 3 and 4
    try:
        driver.switch_to.frame(driver.find_element(
            'xpath', '//*[@id="ivuFrm_page0ivu4"]'))
    except:
        driver.switch_to.frame(driver.find_element(
            'xpath', '//*[@id="ivuFrm_page0ivu3"]'))

    
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
    # sleep(10)

    #switching to working area frame
    driver.switch_to.frame(driver.find_element(
        'xpath', '//*[@id="isolatedWorkArea"]'))

    #It keeps changing to find it again, go to the element, and find the id
    #EG : <input id="WD6A" ....>
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "WD77"))
    )
    driver.find_element('xpath', '//*[@id="WD52"]').send_keys(CONFIG.SESSION)
    driver.find_element('xpath', '//*[@id="WD6E"]').send_keys(CONFIG.SEMESTER)
    driver.find_element('xpath', '//*[@id="WD7B"]').click()

    sleep(8)
    #open csv file attndance.csv and create writer object
    with open(f'attndance_{roll}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        details_list = []
        i = 2
        while 1:
            try:
                details_list.append(driver.find_element('xpath', f'/html/body/table/tbody/tr/td/div/div[1]/span/span[3]/div/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/th[{i}]/div/table/tbody/tr/td/div/span/span').text)
                i = i + 1
            except:
                break
        total_class_index = details_list.index('Total No. of Days')
        absent_class_index = details_list.index('No.of Absent')
        details_list.append('Absents affordable')
        details_list.append(ctime())
        writer.writerow(details_list)
        var = 2
        while 1:
            try:
                details_list = []
                i = 2
                while 1:
                    try:
                        details_list.append(driver.find_element('xpath', f'/html/body/table/tbody/tr/td/div/div[1]/span/span[3]/div/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[{var}]/td[{i}]/span/span').text)
                        i = i + 1
                    except:
                        break
                abs_days = float(details_list[absent_class_index])
                total = float(details_list[total_class_index])
                perc = (abs_days/total) *100
                while perc <= 25:
                    abs_days = abs_days +1
                    total = total +1
                    perc = (abs_days/total) *100
                details_list.append(int(abs_days-float(details_list[absent_class_index])-1))
                writer.writerow(details_list)
                print(details_list)
            except:
                break    
            var  = var +1

    driver.quit()



