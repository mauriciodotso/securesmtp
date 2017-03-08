import smtplib
import email.utils
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'hashedemail'))
msg['From'] = email.utils.formataddr(('Author', 'hashedemail'))
msg['Subject'] = 'Simple test message'

server = smtplib.SMTP('127.0.0.1', 9999)
server.set_debuglevel(True)  # show communication with the server
try:
    server.sendmail('hashedemail', ['hashedemail'],
                    msg.as_string())
finally:
    server.quit()
