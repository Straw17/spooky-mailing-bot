import smtplib, imapclient, pyzmail, random, time, re, os
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime

MEME_DIR = "C:\\Users\\ejcu8\\Desktop\\Python Programs\\Mailing List Bot\\Memes\\"
MEMES = [os.path.join(MEME_DIR, meme) for meme in os.listdir(MEME_DIR)]
LET_LEAVE = 'yes'
PASSWORD = input('Password: ')

def getMailingList():
    file1 = open('MailingList.txt', 'r')
    mailingList = file1.read()
    file1.close()
    mailingList = mailingList.replace("'", '')
    mailingList = mailingList.replace("[", '')
    mailingList = mailingList.replace("]", '')
    mailingList = mailingList.replace("\\r", '')
    mailingList = mailingList.replace("\\n", '')
    mailingList = mailingList.replace(" ", '')
    mailingList = mailingList.split(',')
    return mailingList

def sendMeme(user):
    newMeme = MEMES[random.randint(0, len(MEMES)-1)]
    msg = MIMEMultipart()
    msg['To'] = user
    msg['From'] = 'strawbot17@gmail.com'
    msg['Subject'] = 'Spooky Mailing List: New Meme'
    htmlMsgText = '<html><body><img src="cid:newmeme"><p>Time: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p></body></html>'
    msgText = MIMEText(htmlMsgText, 'html')
    msg.attach(msgText)

    extension = os.path.splitext(newMeme)[1][1:]
    fp = open(newMeme, 'rb')
    image = MIMEImage(fp.read(), _subtype=extension)
    fp.close()
    image.add_header('Content-ID', '<newmeme>')
    msg.attach(image)
    
    server.sendmail('strawbot17@gmail.com', user, msg.as_string())
    print(str(currentTime) + ': Meme sent to ' + user)

def sendIntro(added, adder):
    msg = MIMEMultipart()
    msg['To'] = added
    msg['From'] = 'strawbot17@gmail.com'
    msg['Subject'] = 'Spooky Mailing List: BACK FROM THE GRAVE'
    htmlMsgText = open('intro.html', 'r').read()
    htmlMsgText = htmlMsgText.format(adder, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    msgText = MIMEText(htmlMsgText, 'html')
    msg.attach(msgText)

    fp = open("Skeleton.png", 'rb')
    image = MIMEImage(fp.read(), _subtype="png")
    fp.close()
    image.add_header('Content-ID', '<skeleton>')
    msg.attach(image)

    server.sendmail('strawbot17@gmail.com', added, msg.as_string())
    print(str(currentTime) + ': Welcome sent to ' + added)

file1 = open('MailingList.txt', 'r')
file2 = open('MemeCal.txt', 'r')

server = smtplib.SMTP('smtp.gmail.com', 587)
server.connect("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login('strawbot17@gmail.com', PASSWORD)
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login('strawbot17@gmail.com', PASSWORD)

sEmail = re.compile(r'(?<!\w)[a-z]{4}\d@k12albemarle.org')

mailingList = getMailingList()
print(mailingList)

memeCal = file2.read()
file2.close()
memeCal = memeCal.replace("'", '')
memeCal = memeCal.replace("[", '')
memeCal = memeCal.replace("]", '')
memeCal = memeCal.replace("\\r", '')
memeCal = memeCal.replace("\\n", '')
memeCal = memeCal.split(',')
for day in range(len(memeCal)):
    if memeCal[day][0] == ' ':
        memeCal[day] = memeCal[day][1:]

##if input('Do you want to send an email to the mailing list?\n').lower() == 'yes':
##    sub = input('Subject: ')
##    body = input('Body: ')
##    for user in mailingList:
##        server.sendmail('strawbot17@gmail.com', user, 'Subject: ' + sub + '\n' + body)
##        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
##        print(str(currentTime) + ': Message sent to ' + user)

while True:
    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #update current time
    ##print(currentTime)
    imapObj.select_folder('INBOX', readonly = False) #open inbox and find unread messages
    newMessages = imapObj.search(['UNSEEN'])
    if currentTime[17:19] == '30': #check every 60 seconds
        ##print(str(currentTime) + ': ' + str(server.ehlo())) #print server status
        for day in memeCal: #cycle through days in meme calendar
            currentTime = datetime.strptime(str(currentTime), '%Y-%m-%d %H:%M:%S')
            dayNum = datetime.strptime(day, '%Y-%m-%d %H:%M:%S') 
            if currentTime > dayNum: #proceed if the current time is after the sending time
                for user in mailingList: #cycle through each user in the mailing list, send them a random meme, and log it
                    sendMeme(user)
                    time.sleep(0.5) #sleep for a half second
                memeCal.remove(str(day)) #remove the day
                file2 = open('MemeCal.txt', 'w')
                file2.write(str(memeCal))
                file2.close()
                print(str(currentTime) + ': MemeCal.txt updated')

    currentTime = str(currentTime)
    for message in newMessages: #cycle through new messages
        messages = imapObj.fetch(message, ['BODY[]']) #fetch messages and info
        msg = pyzmail.PyzMessage.factory(messages[message][b'BODY[]'])
        user = msg.get_addresses('from')[0][0]
        sender = msg.get_addresses('from')[0][1]
        oldText = msg.text_part.get_payload().decode(msg.text_part.charset)
        text = oldText.split('\n')
        try: #check for various commands and log
            if '!leave' in text[0]:
                if letLeave == 'no':
                    server.sendmail('strawbot17@gmail.com', sender, 'Subject: Spooky Mailing List\nThis action is not available to users in your country.\nTo apologize for this inconvenience, you will now be sent an extra meme each day.')
                    mailingList.append(sender)
                    file1 = open('MailingList.txt', 'w')
                    file1.write(str(mailingList))
                    file1.close()
                    mailingList = getMailingList()
                    print(currentTime + ': ' + user + ' attempted to leave')
                else:
                    mailingList.remove(sender)
                    file1 = open('MailingList.txt', 'w')
                    file1.write(str(mailingList))
                    file1.close()
                    mailingList = getMailingList()
                    print(currentTime + ': ' + user + ' left')
            elif '!add ' in text[0]:
                newPeople = sEmail.findall(str(text[0]))
                for newPerson in newPeople:
                    if newPerson not in mailingList:
                        sendIntro(newPerson, user)
                        mailingList.append(newPerson)
                        file1 = open('MailingList.txt', 'w')
                        file1.write(str(mailingList))
                        file1.close()
                        print(currentTime + ': MailingList.txt updated')
                        print(currentTime + ': ' + newPerson + ' added to mailing list by ' + user)
                        print(currentTime + ': The current mailing list is: ' + str(mailingList))
            elif '!getNewMeme' in text[0]:
                sendMeme(sender)
            server.sendmail('strawbot17@gmail.com', 'ejcu8@k12albemarle.org', 'Subject: Message from ' + user + '\n' + oldText)
            print(currentTime + ': Message from ' + user + ' sent to master account')
        except ZeroDivisionError:
            print(currentTime + ': Error')
server.quit() #end if loop is somehow broken
