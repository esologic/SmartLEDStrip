from smtplib import SMTP
import subprocess
from time import sleep

def email():
    fromaddr = 'junkb61@gmail.com'
    toaddrs = 'dev@esologic.com'
    username = ''
    password = ''
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("junkb61@gmail.com", "115.junkb61!")

    print('Sending Email')
    SUBJECT = 'Pi Has Booted'
    TEXT = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE).communicate()[0]
    msg = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    print('Email Sent \n')

if __name__ == "__main__":
    sleep(60*1)
    email()