from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
from datetime import datetime
from random import randint, choice, sample
from nord import randNordNow

def initialize(mode=''):
    
    # update log
    with open('log.txt','a') as f:
        dt_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        message = dt_string + '\n' + '>>> initializing browser' + '\n'
        f.write(message)

    if mode == 'headless':
        ff_options = Options()
        ff_options.headless = True
        #ff_options.set_preference('profile','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0')
        ff_options.add_argument("window-size=1920x1080")
        ff_options.add_argument("--start-maximized")
        browser = webdriver.Firefox(options=ff_options)
        browser.maximize_window()
    else:
        browser = webdriver.Firefox()
    
    browser.set_script_timeout(120)
    
    return browser


def fillForm(link,browser,wait):
    
    # open broswer
    browser.get(link)

    with open('log.txt','a') as f:
        message = f'opening link: {link}' + '\n'
        f.write(message)

    # wait for it to load cookie check and close it
    #time.sleep(10)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'html body div#onetrust-consent-sdk div#onetrust-banner-sdk.otFlat.bottom.ot-wo-title.ot-buttons-fw div div#onetrust-close-btn-container'))).click()
    except:
        pass
    
    # wait and then open share feedback form
    time.sleep(4)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/main/div/div/div[2]/div/div/p[52]/a'))).click()
    
    # wait for the new tab to load and switch to it
    time.sleep(10)

    
    with open('log.txt','a') as f:
        message = 'swithcing tabs to form' + '\n'
        f.write(message)

    tabs = browser.window_handles
    browser.switch_to.window(tabs[-1])

    # choose random city
    cities = ['Cardiff','Edinburgh','London','Manchester']
    countryList = browser.find_element(By.ID, "City")
    select = Select(countryList)
    randCity = choice(cities)
    select.select_by_visible_text(randCity)
    
    with open('log.txt','a') as f:
        message = f'random city chosen: {randCity}' + '\n'
        f.write(message)

    # click next button and wait
    browser.find_element(by=By.ID,value='btnNext').click()
    time.sleep(2)

    # fill form
    browser.find_element(By.XPATH,'//*[@id="4"]').click()
    browser.find_element(By.XPATH,'/html/body/div[1]/div/form/fieldset[2]/div[2]/div/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[5]/img').click()
    browser.find_element(By.XPATH,'/html/body/div[1]/div/form/fieldset[2]/div[2]/div/div[1]/div/div[3]/a/div[2]/div/div/ul/li[5]/img').click()
    time.sleep(3)
    randomComplaints()
    browser.find_element(By.ID,'step3-radio-no').click()
    browser.find_element(By.ID,'step5-radio-no').click()
    browser.find_element(By.ID,'btnSubmit').click()

    with open('log.txt','a') as f:
        message = '>>> successfully submitted form' + '\n'
        f.write(message)

    time.sleep(3)

def randomComplaints():

    # filter ptags:
    acceptabeTags1 = ['appointment system','information details','navigation','online application form','online passport tracking services']
    acceptabeTags2 = ['adequate information on the service was available','variety in services offered to ease my submission','ease in purchase of service','value of money']
    tags2Click = []
    allPTags = browser.find_elements(by=By.TAG_NAME,value='p')
    for i in allPTags:
        if i.text.lower().strip('.') in acceptabeTags1:
            tags2Click.append(i)
        if i.text.lower().strip('.') in acceptabeTags2:
            tags2Click.append(i)
    noOfChoices = randint(3, 9)
    
    choices2Click = sample(tags2Click, noOfChoices)
    choicesSelected = []
    for i in choices2Click:
        try:
            time.sleep(1)
            i.click()
            choicesSelected.append(i.text)
        except:
            pass


    with open('log.txt','a') as f:
        message = f'Complaints selected: {len(choicesSelected)}' + '\n'
        f.write(message)
        for ind, val in enumerate(choicesSelected):
            f.write(f'\t{ind+1}) {val}\n')



if __name__ == '__main__':
    
    link = 'https://visa.vfsglobal.com/gbr/en/cyp/contact-us'
    
    while True:
        print('Initiating run...')
        randomTime = randint(1,30)
        
        try:
            # init browseri
            browser = initialize(mode='headless')
            
            # define wait
            wait = WebDriverWait(browser, 120)
    
            # submit
            fillForm(link, browser, wait)
    
            browser.quit()
            print('run successful!')

            with open('numbersubmitted.txt','r+') as track:
                current = int(track.read(1))
                update = str(current + 1)
                track.seek(0)
                track.write(update)
        
            with open('log.txt','a') as f:
                message = f'~~~~~~~~ sleep for {randomTime} seconds ~~~~~~~~\n'
                print(message.rstrip('\n'))
                f.write(message)
        
            time.sleep(randomTime)
        except:
            with open('log.txt') as f:
                message = 'xxx run terminated xxx\n'
                print(message.rstrip('\n'))
                f.write(message)
        
        if choice([False, False, True]):
            newCountry = randNordNow()
            with open('log.txt','a') as f:
                message = f'--------> switching VPN to {newCountry} <--------\n'
                f.write(message)
