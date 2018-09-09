from bs4 import BeautifulSoup
import requests
from time import gmtime, strftime
import time
import datetime
import random
import sys
import dovIncMail


## Setup Variables:
arguments = sys.argv[1:]

runMode = arguments[0] #test, test2, normal
currType = arguments[1] #USD, EUR

if (len(arguments) >= 4):
	refreshDuration = int(arguments[3])
else: 
	refreshDuration = 120 #(4:38)

sendMailDuration = 120



## Programme Variables
baseMoney = 250 #almak istediğim döviz miktarı
if (len(arguments) == 4):
	baseCurr = float(arguments[2])
else: 
	baseCurr  = 4.950000

diffMoneyTL = 0
presentMoneyTL = 0.000000  #baseCurr * baseMoney
sentTime = datetime.datetime(2008, 11, 22, 19, 53, 42) #datetime.datetime.now()
fileName = 'qnb' + currType + datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + '.txt'

## Constant Variables:
count = 0
url = "https://www.qnbfinansbank.enpara.com//doviz-kur-bilgileri/doviz-altin-kurlari.aspx"
bankName = "EnPara"

print("\nRun Mode: " + runMode, " refreshDuration: " + str(refreshDuration) + " sendMailDuration: " + str(sendMailDuration))


	
def getCurrencies(mode):
    global UsdSatis
    global EurSatis
    global UsdAlis
    global EurAlis

    global ConstMoneyTL


    ## Test1: Webe hiç gitme, random kur üret.
    if mode == "test":
        UsdSatis = random.uniform(6, 7)
        EurSatis  = random.uniform(7, 8)
        UsdAlis = random.uniform(6, 6.3)
        EurAlis  = random.uniform(7, 7.3)
        ConstMoneyTL = baseCurr * baseMoney
        return

    try:
        r  = requests.get(url ,headers={"User-Agent":"Mozilla/5.0"})
    except ConnectionError:
        print("Catched ConnectionError in the getCurrencies() method !!!")
            
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    div = soup.find("div", id="pnlContent")

    UsdAlis = float(div.text[4:13].replace(',','.'))
    UsdSatis = float(div.text[16:25].replace(',','.'))

    EurAlis = float(div.text[31:39].replace(',','.'))
    EurSatis = float(div.text[43:51].replace(',','.'))

    ## Test2: Webden gerçek kuru al, ama random eksilt.
    if (mode == "test2"):
        UsdSatis -= random.uniform(0.01, 0.2)
        EurSatis -= random.uniform(0.01, 0.2)
        UsdAlis -= random.uniform(0.01, 0.2)
        EurAlis -= random.uniform(0.01, 0.2)

    ConstMoneyTL = baseCurr * baseMoney

def setCurrTypeRates():
    global currTypeSatis
    global currTypeAlis 
    #currTypeSatis = 0.000000
    #currTypeAlis = 0.000000
	
	#Set Curreny Type for Satis
    if (currType == 'USD'):
        currTypeSatis = UsdSatis
        currTypeAlis = UsdAlis
    elif (currType == 'EUR'):
        currTypeSatis = EurSatis
        currTypeAlis = EurAlis

try:

    #Güncel Kuru Göster:
    getCurrencies(runMode)
    setCurrTypeRates()
    text = ("\nGüncel Kur ", currType, ": %f" % currTypeSatis)
	
    # Kullanıcıdan değerleri al:
    #baseMoney = float(input("(baseMoney) Döviz Miktarı Giriniz: "))
    #baseCurr = float(input("(baseCurr) Temel Kuru Giriniz: "))
    #diffMoneyTL = float(input("(diffMoneyTL) Kaç TL daha ucuza almak istersiniz: "))


## Bilgilendirme Bölümü:
    getCurrencies(runMode)
    setCurrTypeRates()

    text = text + ("\nSatın alınacak doviz tutarı: %d" % baseMoney,)
    text = text + ("\nSabit Kur: %f" % baseCurr, " TL Karşılığı: %f" % ConstMoneyTL)
    text = text + ("\nTL daha az: %f" % diffMoneyTL, " Yani: %f" % (ConstMoneyTL - diffMoneyTL))
    
    currToReach = (ConstMoneyTL - diffMoneyTL) / baseMoney
    text = text + ("\nHedef Kur: %f" % currToReach,)

    time.sleep(refreshDuration)

    ## Write headers to file:
    outputText = ("\nTarih,Saat,Alis Kuru,Satis Kuru,Ederi,Fark,DecAlert\n")
    f = open(fileName, 'a', encoding="utf-8")
    f.write(''.join(text)+outputText)
    f.close()


    while True:
        count += 1
        #print("---------------------------- %d" % count)

        getCurrencies(runMode)
        setCurrTypeRates()
        oldNewCurrDiff = (currTypeSatis - baseCurr)
        diffTL = oldNewCurrDiff * baseMoney
        #print("UsdSatis: ", UsdSatis)
        #print("baseCurr: ", baseCurr)
        
		#Calculate TL equavalent of the currency:
        presentMoneyTL = currTypeSatis * baseMoney

        currDateTime = datetime.datetime.now() ###strftime("%Y-%m-%d %H:%M:%S", gmtime())
        currDate = currDateTime.strftime('%Y-%m-%d')
        currTime = currDateTime.strftime('%H:%M:%S')
        # Alert Control:
        if (presentMoneyTL <= ConstMoneyTL - diffMoneyTL):
            #print("ALERT !!!")
            alertDec = True
        else:
            alertDec = False
		   
#Tarih,Saat,Alis,Satis,Ederi,Fark,DecAlert
        outputText = currDate + "," + currTime + "," + str(round(currTypeAlis,6)) + "," +str(round(currTypeSatis,6)) + "," +  '"' + "{0:,.2f}".format(round(presentMoneyTL,2)) + '",' + str(round(diffTL,2)) + "," + str(alertDec) + "\n"

        ## Write to file:
        f = open(fileName, 'a')
        f.write(outputText)
        f.close()

        ## If Alert is True then send e-mail:
        if (alertDec == True):
            nowTime = datetime.datetime.now()
            ## Prevent send lots of mails
            if (nowTime - sentTime).seconds > sendMailDuration:
                ## Send Mail:
                dovIncMail.sendMail(bankName, currType, round(currTypeSatis,6), baseMoney, round(presentMoneyTL,2))
                sentTime = datetime.datetime.now()
                #print("Mail sent.")
            

        time.sleep(refreshDuration)
        
except KeyboardInterrupt:
    print("Acil Çıkış")

finally:
        print("The End")
        try:
                fUsd.close()
                fEur.close()
                print("File is closed: " + fileName)
        except NameError:
                print("File is already closed: " + fileName)

##print(UsdAlis)
##print(UsdSatis)
##
##print(EurAlis)
##print(EurSatis)

#Notlar: Artıp azalabilir, o ana göre kaç TL azalmış-çoğalmış o da yazsın.

#DateTime ekle...
#print(soup.prettify())

#for link in soup.find_all('span'):
#    print(link.text)
