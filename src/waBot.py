from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sqlite3 as db
import time

def answer(code):
    result = ''
    c = conn.cursor()
    data = c.execute("SELECT answer FROM RESPONSE WHERE code=?", code)
    for row in data:
        result = row[0]
        break
    return result

def check_code(code):
    result = False
    c = conn.cursor()
    data = c.execute("SELECT * FROM RESPONSE WHERE code=?", [code])
    for row in data:
        print(row[0],row[1],row[2])
        if row[0] == code:
            result = True
        else:
            result = False
    return result

def idle(standBy):
    search = driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
    search.send_keys("StandBy")
    try:
        wait5.until(EC.presence_of_element_located((
            By.XPATH, standBy
        )))
    except:
        time.sleep(0.7)
        pass
    driver.find_element_by_xpath(standBy).click()
    driver.find_element_by_css_selector('.C28xL').click()

def main():
    try:
        content = driver.find_element_by_css_selector('.CxUIE')
        content.click()
        
        msg_got = driver.find_elements_by_css_selector("span.selectable-text.invisible-space.copyable-text")
        msg = [message.text for message in msg_got]
        standBy = '//span[contains(@title,"StandBy")]'
        msg = ''.join(e for e in msg[-1] if e.isalnum())
        codeMsg = msg.upper()

        if check_code(codeMsg) == True:
            reply = driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')
            reply.clear()
            reply.click()
            ActionChains(driver).send_keys(answer(codeMsg)).perform()
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ActionChains(driver).send_keys("Ketik *MENU* untuk melihat daftar pertanyaan, atau ketik *SELESAI* untuk mengakhiri perbincangan.").perform()
            time.sleep(0.5)
            ActionChains(driver).send_keys(Keys.RETURN).perform()

            idle(standBy)
        elif codeMsg == "SELESAI":
            time.sleep(0.5)
            idle(standBy)
        else:
            quest = question()
            reply = driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')
            reply.clear()
            reply.click()
            for line in quest.split('\n'):
                ActionChains(driver).send_keys(line).perform()
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            time.sleep(0.5)
            ActionChains(driver).send_keys(Keys.RETURN).perform()

            idle(standBy)

    except NoSuchElementException:
        print('No Unread Message ... Waiting ...')
        pass
    time.sleep(1)

def question():
    result = 'Halo, apa saja sih yang ingin kamu ketahui?\n'
    c = conn.cursor()
    data = c.execute("SELECT * FROM RESPONSE")
    for row in data:
        result = result + "*" + row[0] + "*" + ". " + row[1] + "\n"
    #     result.append([row[0], row[1]])
    result = result + "ketik Abjad (A, B, dst) yang diinginkan jawabannya, kemudian kirim ke kami. Maka, kami akan menjawab pertanyaan kamu."
    return result

if __name__ == '__main__':
    conn = db.connect('db.db')
    
    driver = webdriver.Chrome('C:\\Users\\lufri\\Anaconda3\\projects\\nts-wa-bot\\driver\\chromedriver')
    driver.get('https://web.whatsapp.com/')
    print('Pindai QR Code kemudian tekan enter')
    input()
    
    wait5 = WebDriverWait(driver, 5)
    
    while True:
        main()

    conn.close()
