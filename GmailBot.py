import smtplib, imapclient, pyzmail, random, time
from datetime import datetime

MEMES = []
LET_LEAVE = 'yes'
PASSWORD = input('Password: ')

def getMailingList(file1):
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
tEmail = re.compile(r'(?<!\w)[a-z]{4,}@k12albemarle.org')

mailingList = getMailingList(file1)

##memeCal = file2.read()
##file2.close()
##memeCal = memeCal.replace("'", '')
##memeCal = memeCal.replace("[", '')
##memeCal = memeCal.replace("]", '')
##memeCal = memeCal.replace("\\r", '')
##memeCal = memeCal.replace("\\n", '')
##memeCal = memeCal.split(',')
##for day in range(len(memeCal)):
##    if memeCal[day][0] == ' ':
##        memeCal[day] = memeCal[day][1:]

##if input('Do you want to send an email to the mailing list?\n').lower() == 'yes':
##    sub = input('Subject: ')
##    body = input('Body: ')
##    for user in mailingList:
##        server.sendmail('strawbot17@gmail.com', user, 'Subject: ' + sub + '\n' + body)

while True:
    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ##print(currentTime)
    imapObj.select_folder('INBOX', readonly = False)
    newMessages = imapObj.search(['UNSEEN'])
    if currentTime[17:19] == '30':
        print(str(currentTime) + ': ' + str(server.ehlo()))
        for day in memeCal:
            currentTime = datetime.strptime(str(currentTime), '%Y-%m-%d %H:%M:%S')
            day = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
            if currentTime > day:
                for user in mailingList:
                    newMemeID = random.randint(0, len(memes)-1)
                    server.sendmail('strawbot17@gmail.com', user, 'Subject: Spooky Mailing List\nHere is your new meme\n' + memes[newMemeID])
                    print(str(currentTime) + ': Bidaily meme sent to ' + user)
                memeCal.remove(str(day))
                file2 = open('MemeCal.txt', 'w')
                file2.write(str(memeCal))
                file2.close()
                print(str(currentTime) + ': MemeCal updated')
        time.sleep(1)
    currentTime = str(currentTime)
    for message in newMessages:
        messages = imapObj.fetch(message, ['BODY[]'])
        msg = pyzmail.PyzMessage.factory(messages[message][b'BODY[]'])
        userName = msg.get_addresses('from')[0][0]
        sender = msg.get_addresses('from')[0][1]
        oldText = msg.text_part.get_payload().decode(msg.text_part.charset)
        text = oldText.split('\n')
        try:
            if '!help' in text[0]:
                server.sendmail('strawbot17@gmail.com', sender, 'Subject: Spooky Mailing List\n!add    Add an email to the mailing list\n!getNewMeme   Get a new meme\n!leave   Leave the mailing list')
                print(currentTime + ': ' + userName + ' requested help')
            elif '!leave' in text[0]:
                if letLeave == 'no':
                    server.sendmail('strawbot17@gmail.com', sender, 'Subject: Spooky Mailing List\nThis action is not available to users in your country.\nTo apologize for this inconvenience, you will now be sent two extra memes each day.')
                    mailingList.append(sender)
                    file1 = open('MailingList.txt', 'w')
                    file1.write(str(mailingList))
                    file1.close()
                    mailingList = getMailingList(file1)
                    print(currentTime + ': ' + userName + ' attempted to leave')
                else:
                    mailingList.remove(sender)
                    file1 = open('MailingList.txt', 'w')
                    file1.write(str(mailingList))
                    file1.close()
                    mailingList = getMailingList(file1)
                    print(currentTime + ': ' + userName + ' left')
            elif '!add ' in text[0]:
                sEmails = sEmail.findall(text)
                tEmails = tEmail.findall(text)
                newPeople = sEmails + tEmails
                for newPerson in newPeople:
                    if newPerson not in mailingList:
                        if newPerson not in tEmails:
                            server.sendmail('strawbot17@gmail.com', newPerson, 'Subject: Spooky Mailing List\nYou have been added to the Spooky Mailing List by ' + userName + "!\nYou will be regularly recieving spooky memes!\nEnter !help for a list of commands.\nI don't care if the bot does weird stuff.")
                            mailingList.append(newPerson)
                            file1 = open('MailingList.txt', 'w')
                            file1.write(str(mailingList))
                            file1.close()
                            mailingList = getMailingList(file1)
                            print(currentTime + ': MailingList updated')
                        
                print(currentTime + ': ' + newPerson + ' added to mailing list by ' + userName)
                print(currentTime + ': The current mailing list is: ' + str(mailingList))
            elif '!getNewMeme' in text[0]:
                newMemeID = random.randint(0, len(memes)-1)
                server.sendmail('strawbot17@gmail.com', sender, 'Subject:Spooky Mailing List\nHere is your new meme\n' + memes[newMemeID])
                print(currentTime + ': New meme requested by ' + userName)
            server.sendmail('strawbot17@gmail.com', 'ejcu8@k12albemarle.org', 'Subject: Message from ' + userName + '\n' + oldText)
            print(currentTime + ': Message from ' + userName + ' sent to master account')
        except Exception:
            print(currentTime + ': Error')
server.quit()
