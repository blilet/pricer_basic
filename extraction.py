import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
import time
options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome('C:/change/commun/chromedriver.exe', options=options)
def GetFXRates():
    website = 'https://www.dailyfx.com/forex-rates#currencies'
    driver.get(website)
    time.sleep(1)
    changes = driver.find_elements(By.CSS_SELECTOR, '.dfx-singleInstrument__name')
    k=0
    for i in range(len(changes)):
        if changes[i].text == 'Gold':
            k=i
            break
    changes = changes[0:k]
    ratesLow = driver.find_elements(By.CSS_SELECTOR, '.dfx-singleInstrument__price.dfx-rate.dfx-font-size-3.dfx-font-size-lg-4.font-weight-bold.text-right')
    ratesHigh =driver.find_elements(By.CSS_SELECTOR, '.dfx-singleInstrument__price.dfx-rate.dfx-singleInstrument__priceAsk.text-secondary.text-right')
    out = []
    for x in changes:
        if x.text=='': changes.remove(x)
    for i in range(len(changes)):
        out +=[[changes[i].text] + [ratesLow[2*i].get_attribute("data-value")]+[ratesHigh[2*i].get_attribute("data-value")]]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
    return [current_time,out]
def GetEURIBAR():
    website = 'https://www.boursorama.com/bourse/taux/court-terme/euribor'
    driver.get(website)
    time.sleep(1)
    taux = driver.find_elements(By.CSS_SELECTOR, '.c-instrument.c-instrument--last')[1:]
    out =[]
    for i in range(len(taux)):
        out+=[taux[i].text]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [current_time, out]
def GetLIBRO():
    website = 'https://www.global-rates.com/fr/taux-de-interets/libor/libor.aspx'
    driver.get(website)
    time.sleep(1)
    accept = driver.find_element(By.CLASS_NAME, 'fc-button-label')
    accept.click()
    time.sleep(1)
    overnight = driver.find_element(By.XPATH, '/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[2]/td[2]').text
    oneMonth = driver.find_element(By.XPATH,'/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[3]/td[2]').text
    threeMonths = driver.find_element(By.XPATH,'/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[4]/td[2]').text
    sixMonths= driver.find_element(By.XPATH,'/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[5]/td[2]').text
    twelveMonths = driver.find_element(By.XPATH, '/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[6]/td[2]').text
    datum = driver.find_element(By.XPATH,'/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[5]/tbody/tr[1]/td[2]/span').text
    return [datum] + [[overnight, oneMonth, threeMonths, sixMonths, twelveMonths]]
def GetMA():
    website = 'https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Taux-de-reference-du-marche-interbancaire'
    driver.get(website)
    time.sleep(3)
    taux = driver.find_elements(By.CSS_SELECTOR, '.number')
    out =[]
    for i in range(len(taux)//2):
        out+= [[taux[2*i].text,taux[2*i+1].text]]
    out.reverse()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [current_time,out]
def GetVolat():
    website = 'https://fxowebtools.saxobank.com/otc.html'
    driver.get(website)
    time.sleep(3)
    out=[]
    for i in range(2,13):
        temp = driver.find_element(By.XPATH, './html/body/div[3]/table/tbody/tr['+str(i)+']').text.split(" ")
        tempL =[]
        for j in range(len(temp)):
            if '(' in temp[j]: continue
            else: tempL += [temp[j]]
        out.append(tempL)
    return out
def GetSpotMAEUR():
    website = 'https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-des-changes/Cours-de-change/Cours-de-reference'
    driver.get(website)
    time.sleep(0.1)
    taux = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[4]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/span')
    out = taux.text
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [current_time,out]
print(GetFXRates())
