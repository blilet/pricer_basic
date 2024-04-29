from math import sqrt #Importation de la fonction sqrt du module math
from math import log #Importation de la fonction log du module math
from math import exp #Importation de la fonction exp du module math
import scipy
import scipy.stats as stats
import numpy as np
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
driver = webdriver.Chrome(r'/usr/bin/chromedriver', options=options)
def cox_ross_rubinstein_call(S, K, r, T, sigma, N):
    dt = T/N
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt) - d) / (u - d)
    stock_price = np.zeros((N+1, N+1))
    option_price = np.zeros((N+1, N+1))
    stock_price[0, 0] = S
    for i in range(1, N+1):
        stock_price[i, 0] = stock_price[i-1, 0] * u
        for j in range(1, i+1):
            stock_price[i, j] = stock_price[i-1, j-1] * d
    for j in range(N+1):
        option_price[N, j] = max(0, stock_price[N, j] - K)
    for i in range(N-1, -1, -1):
        for j in range(i+1):
            option_price[i, j] = (p * option_price[i+1, j] + (1-p) * option_price[i+1, j+1]) / np.exp(r*dt)
    return option_price[0, 0]
def cox_ross_rubinstein_put(S, K, r, T, sigma, N):
    dt = T/N
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt) - d) / (u - d)
    stock_price = np.zeros((N+1, N+1))
    option_price = np.zeros((N+1, N+1))
    stock_price[0, 0] = S
    for i in range(1, N+1):
        stock_price[i, 0] = stock_price[i-1, 0] * u
        for j in range(1, i+1):
            stock_price[i, j] = stock_price[i-1, j-1] * d
    for j in range(N+1):
        option_price[N, j] = max(0, K - stock_price[N, j])
    for i in range(N-1, -1, -1):
        for j in range(i+1):
            option_price[i, j] = (p * option_price[i+1, j] + (1-p) * option_price[i+1, j+1]) / np.exp(r*dt)
    return option_price[0, 0]
def monte_carlo_put(S, K, r, sigma, T, n_simulations):
    # Calcul des paramètres pour la simulation
    dt = T / 365.0
    n_steps = int(T / dt)
    discount_factor = np.exp(-r * T)

    # Simulation de Monte Carlo
    s = np.zeros((n_simulations, n_steps))
    s[:, 0] = S
    for i in range(1, n_steps):
        s[:, i] = s[:, i-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=n_simulations))

    # Calcul de la valeur de l'option
    payoffs = np.maximum(K - s[:, -1], 0)
    option_price = discount_factor * np.mean(payoffs)

    return option_price
def monte_carlo_call(S, K, r, sigma, T, M):
    dt = T / 252  # 252 jours ouvrables dans une année
    drift = np.exp((r - 0.5 * sigma ** 2) * dt)
    stdev = sigma * np.sqrt(dt)

    prices = np.zeros(M)

    for i in range(M):
        shock = np.random.normal(0, 1)
        price = S * drift ** (1 + shock * stdev)
        prices[i] = price

    payoff = np.maximum(prices - K, 0)
    price = np.exp(-r * T) * np.mean(payoff)

    return price
def GetFXRates():
    website = 'https://www.dailyfx.com/forex-rates#currencies'
    driver.get(website)
    time.sleep(0.1)
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
def GetEURIBOR():
    website = 'https://www.boursorama.com/bourse/taux/court-terme/euribor'
    driver.get(website)
    taux = driver.find_elements(By.CSS_SELECTOR, '.c-instrument.c-instrument--last')[1:]
    out =[]
    for i in range(len(taux)):
        out+=[taux[i].text]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [current_time, out]
def GetLIBOR():
    website = 'https://www.global-rates.com/fr/taux-de-interets/libor/libor.aspx'
    driver.get(website)
    time.sleep(0.2)
    accept = driver.find_element(By.CLASS_NAME, 'fc-button-label')
    accept.click()
    driver.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
    time.sleep(0.2)
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
    time.sleep(0.1)
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
    time.sleep(0.1)
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
#Européene, call, Copenhagen
def d_un(S,K,sigma,T,r,q):#S: (EUR/DOL: getFX) (DOL/MAD - MAD/EUR: TBA), K variable, sigma(T), T variable, r LIBOR(MAD == getMad)(T),q EURIBOR(T)
    d1=(1/(sigma*sqrt(T)))*(log(S/K)+(r-q+(sigma**2)/2)*T)
    return(d1)
def d_deux(S,K,sigma,T,r,q):
    d2 =d_un(S,K,sigma,T,r,q) - (sigma*sqrt(T))
    return(d2)
def bs_call(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    d2=d_deux(S,K,sigma,T,r,q)
    N_d1=stats.norm.cdf(d1, 0, 1)
    N_d2=stats.norm.cdf(d2, 0, 1)
    op_call=(S*exp(-q*T)*N_d1)-(K*exp(-r*T)*N_d2)
    return(op_call)
#Euro, put
def bs_put(S,K,sigma,T,r,q):
    d1=d_un(S,K,sigma,T,r,q)
    d2=d_deux(S,K,sigma,T,r,q)
    N_nd1=stats.norm.cdf(-d1, 0, 1)
    N_nd2=stats.norm.cdf(-d2, 0, 1)
    op_put=(-S*exp(-q*T)*N_nd1)+(K*exp(-r*T)*N_nd2)
    return(op_put)
#Americaine, call, binomiale
##########################################################
import customtkinter
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
customtkinter.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
#window*
window = ctk.CTk()
window.title('Pricer')
window.geometry("280x450")
window.resizable(False, False)
nature = ctk.StringVar(master=window)
nature.set("Choisir")
model = ctk.StringVar(master=window)
model.set("Choisir")
option = ctk.StringVar(master=window)
option.set("Choisir")
paire= ctk.StringVar(master=window)
paire.set("Choisir nature")
mat = ctk.StringVar(master = window)
mat.set("1 mois")
#b1 = ctk.CTkButton(window, text='Raffraîchir données')
#b2 = ctk.CTkButton(window, text='Pricer')
#b1.grid(column=0, row=0)   # grid dynamically divides the space in a grid
#b2.grid(column=1, row=1)
labelN =ctk.CTkLabel(master=window,text="Nature:").grid(column =0, row = 1)
natureDrop=tk.OptionMenu(window, nature, 'Américaine', 'Européenne').grid(column=1, row = 1)
labelO = ctk.CTkLabel(master=window,text="Type d'option:").grid(column =0, row = 2)
optionDrop=tk.OptionMenu(window, option, 'Put', 'Call').grid(column=1, row = 2)
labelPD = ctk.CTkLabel(master=window,text="Paire de devises:").grid(column =0, row = 3)
PDDrop=tk.OptionMenu(window, paire, "Choisir nature").grid(column=1, row = 3)
labelS = ctk.CTkLabel(master=window,text="Spot:").grid(column =0, row = 4)
labelStr = ctk.CTkLabel(master=window,text="Strike:").grid(column =0, row = 5)
strikeInput=ctk.CTkTextbox(window, width=100, height=25)
strikeInput.grid(column=1, row = 5)
labelM = ctk.CTkLabel(master=window,text="Maturité:").grid(column =0, row = 6)
dropM=tk.OptionMenu(window, mat,"1 semaine", "1 mois", "3 mois").grid(column=1, row = 6)
dropModel=tk.OptionMenu(window, model,"Choisir nature:").grid(column=1, row = 10)
labelTD = ctk.CTkLabel(master=window,text="Taux devise domestique:").grid(column =0, row = 7)
labelTE = ctk.CTkLabel(master=window,text="Taux devise étrangère:").grid(column =0, row = 8)
labelV = ctk.CTkLabel(master=window,text="Volatilité:").grid(column =0, row = 9)
labelM= ctk.CTkLabel(master=window,text="Modèle:").grid(column =0, row = 10)
pasA = ctk.CTkTextbox(window, width=100, height=25)
pasA.grid(column=1, row=14)

def data():
    T = 2
    matS = mat.get()
    if matS == "Aujourd'hui": T=0
    elif matS == "1 semaine": T =1
    elif matS == "1 mois": T=2
    elif matS == "3 mois": T=3
    print(strikeInput.get("0.0", "end"))
    nat = nature.get()
    dev = paire.get()

    sigma = float(GetVolat()[0][T + 1])
    labelVolA = ctk.CTkLabel(master=window, text="         ").grid(column=1, row=9)
    labelVol = ctk.CTkLabel(master=window, text=str(sigma)).grid(column=1, row=9)
    Tp = T
    if Tp == 3: Tp = 4
    if nat == 'Européenne':
        labelMod = ctk.CTkLabel(master=window, text="Garman-Kohlhagen").grid(column=1, row=10)
        if dev == 'EUR/USD':
            S= float(GetFXRates()[1][1][2])
            SvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=4)
            Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
            Tp = T
            if Tp == 1: Tp =0
            rEURDOL = float(GetEURIBOR()[1][T-1].replace('%', ''))
            TDvalueA = ctk.CTkLabel(master=window, text="           ").grid(column=1, row=7)
            TDvalue = ctk.CTkLabel(master=window, text=str(rEURDOL)).grid(column=1, row=7)
            q = float(GetLIBOR()[1][Tp].replace(' %', '').replace(',', '.'))
            labelTEQA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=8)
            labelTEQ = ctk.CTkLabel(master=window, text=str(q)).grid(column=1, row=8)
        if dev == 'EUR/MAD':
            S= float(GetSpotMAEUR()[1].replace(',', '.'))
            SvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=4)
            Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
            Tp = T
            if Tp >=2: Tp =Tp-1
            rMAD = float(GetEURIBOR()[1][T-1].replace('%', ''))
            TDvalueA = ctk.CTkLabel(master=window, text="            ").grid(column=1, row=7)
            TDvalue = ctk.CTkLabel(master=window, text=str(rMAD)).grid(column=1, row=7)
            q = float(GetMA()[1][Tp][1].replace(' %', '').replace(',', '.'))
            labelTEQA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=8)
            labelTEQ = ctk.CTkLabel(master=window, text=str(q)).grid(column=1, row=8)
    elif nat == 'Américaine':
        labelModA = ctk.CTkLabel(master=window, text="             ").grid(column=1, row=10)
        labelMod = ctk.CTkLabel(master=window, text="Cox-Ross-Robinstein").grid(column=1, row=10)
        S = float(GetFXRates()[1][2][2])
        SvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=4)
        Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
        Tp = T
        if Tp == 1: Tp = 0
        b=T
        if T == 1:
            b -= 1
        rEURDOL = float(GetEURIBOR()[1][b].replace('%', ''))
        TDvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=7)
        TDvalue = ctk.CTkLabel(master=window, text=str(rEURDOL)).grid(column=1, row=7)
    print("data")
def price():
    T = 2
    maturityAn = 0
    matS = mat.get()
    if matS == "Aujourd'hui":
        T=0
        maturityAn = 1/365
    elif matS == "1 semaine":
        T =1
        maturityAn = 7 / 365
    elif matS == "1 mois":
        T=2
        maturityAn = 30 / 365
    elif matS == "3 mois":
        T=3
        maturityAn = 90 / 365
    print(strikeInput.get("0.0", "end"))
    nat = nature.get()
    mod = model.get()
    dev = paire.get()
    K= float(strikeInput.get('0.0', 'end').replace(' ',''))
    sigma = float(GetVolat()[0][T + 1])
    labelVolA = ctk.CTkLabel(master=window, text="       ").grid(column=1, row=9)
    labelVol = ctk.CTkLabel(master=window, text=str(sigma)).grid(column=1, row=9)
    Tp = T
    if Tp == 3: Tp = 4
    if nat == 'Européenne':
        if dev == 'EUR/USD':
            S= float(GetFXRates()[1][1][2])
            SvalueA = ctk.CTkLabel(master=window, text="       ").grid(column=1, row=4)
            Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
            Tp = T
            q = float(GetLIBOR()[1][Tp].replace(' %', '').replace(',', '.'))
            labelTEQA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=8)
            labelTEQ = ctk.CTkLabel(master=window, text=str(q)).grid(column=1, row=8)
            if Tp == 1: Tp =0
            b= T
            if T == 1:
                b-=1
            rEURDOL = float(GetEURIBOR()[1][b].replace('%', ''))
            TDvalueA = ctk.CTkLabel(master=window, text="       ").grid(column=1, row=7)
            TDvalue = ctk.CTkLabel(master=window, text=str(rEURDOL)).grid(column=1, row=7)
            print(T, K, S, rEURDOL, q)
            c = 100*bs_call(S,K, sigma/100, maturityAn, rEURDOL/100, q/100)
            p = 100*bs_put(S,K, sigma/100, maturityAn, rEURDOL/100, q/100)
            primeV = ''
            if option.get() == "Put": primeV = str(p)
            else: primeV = str(c)
            try:
                primeV = primeV[0:6]
            except:
                print("Moins de 6 caractères")
            primeValueA = ctk.CTkLabel(master=window, text="         ").grid(column=1, row=13)
            primeValue = ctk.CTkLabel(master=window, text=primeV + "%").grid(column=1, row=13)
        if dev == 'EUR/MAD':
            S= float(GetSpotMAEUR()[1].replace(',', '.'))
            SvalueA = ctk.CTkLabel(master=window, text="       ").grid(column=1, row=4)
            Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
            Tp = T
            q = float(GetMA()[1][Tp][1].replace(' %', '').replace(',', '.'))
            labelTEQA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=8)
            labelTEQ = ctk.CTkLabel(master=window, text=str(q)).grid(column=1, row=8)
            if Tp >=2: Tp =Tp-1
            rMAD = float(GetMA()[1][Tp][1].replace(' %', '').replace(',', '.'))
            TDvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=7)
            TDvalue = ctk.CTkLabel(master=window, text=str(rMAD)).grid(column=1, row=7)
            c = 10*bs_call(S,K, sigma/100,maturityAn, rMAD/100, q/100)
            p = 10*bs_put(S,K, sigma/100, maturityAn, rMAD/100, q/100)
            primeV = ''
            if option.get() == "Put": primeV = str(p)
            else: primeV = str(c)
            try:
                primeV = primeV[0:6]
            except:
                print("gucii")
            primeValueA = ctk.CTkLabel(master=window, text="         ").grid(column=1, row=13)
            primeValue = ctk.CTkLabel(master=window, text=primeV + "%").grid(column=1, row=13)
    elif nat == 'Américaine':
        print(pasA.get('0.0', 'end'))
        q = float(GetLIBOR()[1][Tp].replace(' %', '').replace(',', '.'))
        labelTEQA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=8)
        labelTEQ = ctk.CTkLabel(master=window, text=str(q)).grid(column=1, row=8)
        N = int(float(pasA.get('0.0', 'end').replace(' ', '').replace('\n', '')))
        S = float(GetFXRates()[1][1][2])
        SvalueA = ctk.CTkLabel(master=window, text="        ").grid(column=1, row=4)
        Svalue = ctk.CTkLabel(master=window, text=str(S)).grid(column=1, row=4)
        Tp = T
        if Tp == 1: Tp = 0
        TDvalueA = ctk.CTkLabel(master=window, text="       ").grid(column=1, row=7)
        b=T
        if T == 1:
            b -= 1
        rEURDOL = float(GetEURIBOR()[1][b].replace('%', ''))
        TDvalue = ctk.CTkLabel(master=window, text=str(rEURDOL)).grid(column=1, row=7)
        pc = 100*cox_ross_rubinstein_put(S, K,rEURDOL / 100,maturityAn , sigma/100,N)
        cc = 100*cox_ross_rubinstein_call(S, K,rEURDOL / 100,maturityAn , sigma/100,N)
        pm = 100*monte_carlo_put(S,K,rEURDOL/100,sigma/100,maturityAn, N)
        cm = 100*monte_carlo_call(S,K,rEURDOL/100,sigma/100,maturityAn, N)
        primeV = ''
        if mod == "Cox-Ross-Robinstein":
            if option.get() == "Put":
                primeV = str(pc)
            else:
                primeV = str(cc)
            try:
                primeV = primeV[0:6]
            except:
                print("gucii")
        elif mod == "Monte Carlo":
            if option.get() == "Put":
                primeV = str(pm)
            else:
                primeV = str(cm)
            try:
                primeV = primeV[0:6]
            except:
                print("gucii")
        primeValueA = ctk.CTkLabel(master=window, text="         ").grid(column=1, row=13)
        primeValue = ctk.CTkLabel(master=window, text=primeV + "%").grid(column=1, row=13)
def change(*args):
    if nature.get()=="Choisir":
        dropModel = tk.OptionMenu(window, model, "Choisir nature:").grid(column=1, row=10)
        PDDrop=tk.OptionMenu(window, paire, 'Choisir nature').grid(column=1, row = 3)
    elif nature.get() == "Américaine":
        dropModel = tk.OptionMenu(window, model, "Monte Carlo", "Cox-Ross-Robinstein").grid(column=1, row=10)
        PDDrop=tk.OptionMenu(window, paire, 'EUR/USD').grid(column=1, row = 3)
        paire.set('EUR/USD')
        primeLabel = ctk.CTkLabel(master=window, text="Nombre de pas:").grid(column=0, row=14)
    else:
        dropModel = tk.OptionMenu(window, model, "Garman-Kohlhagen").grid(column=1, row=10)
        PDDrop=tk.OptionMenu(window, paire, 'EUR/USD', 'EUR/MAD').grid(column=1, row = 3)
    print(paire.get())
    priceBtn = customtkinter.CTkButton(master=window, text="Pricing", command=price).grid(column=1, row=11)
    dataBtn = customtkinter.CTkButton(master=window, text="Raffraichir données", command=data).grid(column=0, row=11)
    primeLabel = ctk.CTkLabel(master=window, text="Prime:").grid(column=0, row=13)
    primeValue = ctk.CTkLabel(master=window, text="------").grid(column=1, row=13)
nature.trace("w", change)

#run
window.mainloop()
