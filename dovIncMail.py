import smtplib
from email.mime.text import MIMEText
import os
import csv

mailDetails = []
os.chdir("customIgnore")
for row in csv.reader(open("pass.csv","rt", encoding='UTF-8')):       
        mailDetails.append(row)

def sendMail(pBank, pDovSatis, pBaseMoney, pPresentMoneyTL):
    print(mailDetails[0][1])
    print(mailDetails[1][1])
    print(mailDetails[2][1])
    print(mailDetails[3][1])
    print(mailDetails[4][1])
    print(mailDetails[5][1])


    smtpServer = mailDetails[0][1] #smtp.gmail.com:587
    fromMail = mailDetails[1][1] #Readable Name <example@mail.com>
    toMail = mailDetails[2][1] #Readable Name <example@mail.com>
    loginUser = mailDetails[3][1] #Mail User Name
    loginPass = mailDetails[4][1] #Mail User Password
    toEmail = mailDetails[5][1]
    
    title = pDovSatis
    msg_content = '<h2>{title} * <font color="green">{pBaseMoney}$</font> = {pPresentMoneyTL}TL</h2>\n'.format(title=title,pBaseMoney=pBaseMoney,pPresentMoneyTL=pPresentMoneyTL)
    message = MIMEText(msg_content, 'html')

    message['From'] = fromMail
    message['To'] = toMail
    ##message['Cc'] = 'Receiver2 Name <receiver2@server>'
    message['Subject'] = 'DOLARA SALDIR: ' + str(pDovSatis) + " " + pBank

    msg_full = message.as_string()

    server = smtplib.SMTP(smtpServer)
    server.starttls()
    server.login(loginUser, loginPass)
    server.sendmail(loginUser,
                    ['berkaysit@gmail.com', 'berkaysit@gmail.com'],
                    msg_full)
    server.quit()
