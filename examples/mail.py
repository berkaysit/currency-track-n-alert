import smtplib
from email.mime.text import MIMEText

def sendMail():
    title = 'My title'
    msg_content = '<h2>{title} > <font color="green">OK</font></h2>\n'.format(title=title)
    message = MIMEText(msg_content, 'html')

    message['From'] = 'your name <name@gmail.com>'
    message['To'] = 'Receiver Name <Receiver@gmail.com>'
    ##message['Cc'] = 'Receiver2 Name <receiver2@server>'
    message['Subject'] = 'DOLARA SALDIR !!!'

    msg_full = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('loginUser@gmail.com', 'ber.kay2018')
    server.sendmail('name@gmail.com',
                    ['to@gmail.com', 'to@gmail.com'],
                    msg_full)
    server.quit()
