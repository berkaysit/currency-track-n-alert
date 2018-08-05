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
if (len(arguments) == 2):
	refreshDuration = int(arguments[1])
else: 
	refreshDuration = 120 #(4:38)

sendMailDuration = 120
runMode = arguments[0] #test, test2, normal


## Programme Variables
baseMoney = 250 #almak istediğim döviz miktarı
baseCurr  = 4.800000
diffMoneyTL = 0
presentMoneyTL = 0.000000
sentTime = datetime.datetime(2008, 11, 22, 19, 53, 42) #datetime.datetime.now()
fileName = 'zir' + datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + '.txt'


## Constant Variables:
count = 0
url = "https://www.ziraatbank.com.tr/tr/fiyatlar-ve-oranlar"
bankName = "Ziraat"

print("\nRun Mode: " + runMode, " refreshDuration: " + str(refreshDuration) + " sendMailDuration: " + str(sendMailDuration))

def getCurrencies(mode):
    global UsdSatis
    global ConstMoneyTL

    ## Test1: Webe hiç gitme, random kur üret.
    if mode == "test":
        UsdSatis = random.uniform(4.1, 5)
        ConstMoneyTL = baseCurr * baseMoney
        return
        
    try:
        r  = requests.get(url ,headers={"User-Agent":"Mozilla/5.0"})
    except ConnectionError:
        print("Catched ConnectionError in the getCurrencies() method !!!")

    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find_all('table')[8] #.get_text()
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:

        if row.find_all('td')[0].get_text() == 'USD':
            UsdAlis = row.find_all('td')[2].get_text()
            UsdSatis = row.find_all('td')[3].get_text()
##            print("Buldum: " + str(UsdAlis.replace(',','.')) )
##            print("Buldum: " + str(UsdSatis.replace(',','.')) )
            UsdAlis = float(UsdAlis.replace(',','.'))
            UsdSatis = float(UsdSatis.replace(',','.'))

        if row.find_all('td')[0].get_text() == 'EUR':
            EurAlis = row.find_all('td')[2].get_text()
            EurSatis = row.find_all('td')[3].get_text()
##            print("Buldum: " + str(UsdAlis.replace(',','.')) )
##            print("Buldum: " + str(UsdSatis.replace(',','.')) )
            EurAlis = float(EurAlis.replace(',','.'))
            EurSatis = float(EurSatis.replace(',','.'))


    ## Test2: Webden gerçek kuru al, ama random eksilt.
    if (mode == "test2"):
        UsdSatis -= random.uniform(0.01, 0.2)
        
    ConstMoneyTL = baseCurr * baseMoney

try:
    #Güncel Kuru Göster:
    getCurrencies(runMode)
    print("\nGüncel Kur: %f" % UsdSatis)

    # Kullanıcıdan değerleri al:
    #baseMoney = float(input("(baseMoney) Döviz Miktarı Giriniz: "))
    #baseCurr = float(input("(baseCurr) Temel Kuru Giriniz: "))
    #diffMoneyTL = float(input("(diffMoneyTL) Kaç TL daha ucuza almak istersiniz: "))


## Bilgilendirme Bölümü:
    getCurrencies(runMode)
    print("\nSatın alınacak doviz tutarı: %d" % baseMoney)
    print("Sabit Kur: %f" % baseCurr, " TL Karşılığı: %f" % ConstMoneyTL)
    
    print("TL daha az: %f" % diffMoneyTL, " Yani: %f" % (ConstMoneyTL - diffMoneyTL))
    currToReach = (ConstMoneyTL - diffMoneyTL) / baseMoney
    print("Hedef Kur: %f" % currToReach)
    time.sleep(refreshDuration)

    ## Write headers to file:
    outputText = "Tarih,Saat,Kur,Satis,Ederi,Fark,DecAlert\n"
    f = open(fileName, 'a')
    f.write(outputText)
    f.close()    


    while True:
        count += 1
        print("---------------------------- %d" % count)

        getCurrencies(runMode)
        
        oldNewCurrDiff = (UsdSatis - baseCurr)
        diffTL = oldNewCurrDiff * baseMoney
        #print("UsdSatis: ", UsdSatis)
        #print("baseCurr: ", baseCurr)
        
        presentMoneyTL = UsdSatis * baseMoney

        currDateTime = datetime.datetime.now() ###strftime("%Y-%m-%d %H:%M:%S", gmtime())
        currDate = currDateTime.strftime('%Y-%m-%d')
        currTime = currDateTime.strftime('%H:%M:%S')

        if (presentMoneyTL <= ConstMoneyTL - diffMoneyTL):
            #print("ALERT !!!")
            alertDec = True
        else:
            alertDec = False

        outputText = currDate + "," + currTime + "," + str(round(UsdSatis,6)) + "," +  '"' + "{0:,.2f}".format(round(presentMoneyTL,2)) + '",' + str(round(diffTL,2)) + "," + str(alertDec) + "\n"
        #outputText = currTime + ";Kur: " + str(round(UsdSatis,6)) + ";Ederi: " +  "{0:,.2f}".format(round(presentMoneyTL,2)) + ";Fark: " + str(round(diffTL,2)) + ";DecAlert: " + str(alertDec) + "\n"
        print(outputText)
##        print(currTime, ";Kur: %f" % UsdSatis, ";Ederi: %f" % presentMoneyTL, ";Fark: %f" % diffTL, ";DecAlert: ", alertDec)

        ## Write to file:
        f = open(fileName, 'a')
        f.write(outputText)
        f.close()

        ## If Alert True then send e-mail:
        if (alertDec == True):
            nowTime = datetime.datetime.now()
            ## Prevent send lots of mails
            if (nowTime - sentTime).seconds > sendMailDuration:
                ## Send Mail:
                dovIncMail.sendMail(bankName, round(UsdSatis,6), baseMoney, round(presentMoneyTL,2))
                sentTime = datetime.datetime.now()
                #print("Mail sent.")
            

        time.sleep(refreshDuration)
        
except KeyboardInterrupt:
    print("Acil Çıkış")

finally:
        print("The End")
        try:
                f.close()
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
