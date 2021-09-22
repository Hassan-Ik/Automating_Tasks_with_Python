# For http requests
import requests
# Web Scraping
from bs4 import BeautifulSoup
# Sending Mail
import smtplib
# Email Body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Date and Time
import datetime

now = datetime.datetime.now()

# Email Content Placeholder
content = ''

# Extracting Hacker News Stories

def extract_news(url):
    print("Extracting Hacker News Stories.....")
    cnt = ''
    cnt += ('<b>Hacker News Top Stories:</b>\n'+ '<br>' + '-'*50+ '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + '\n' + '<br>') if tag.text != 'More' else '')
    return cnt

cnt = extract_news("https://news.vcombinator.com/")
content += cnt
content += ('<br>--------</br>')
content += ('<br></br>End of Message')

# Lets Send the Email
print("Composing Email......")

# update email details

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM = 'hassanikram555@gmail.com' # your from email id
TO = 'hassanikram08@gmail.com' # your to email id or list of ids
PASS = 'breakitgo1' # your email id password

# fp = open(filename, 'rb')
# Create a text/plain message
# msg = MIMETEXT('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachement', filename='empty.txt')
msg['Subject'] = 'Top Stories Hacker News [Automated Email]' + ' ' + str(now.day) + '-' + str(now.year)

msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initializing Server....')

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent")

server.quit()