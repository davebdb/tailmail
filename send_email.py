#!/usr/bin/python
import smtplib
import argparse
import socket
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, files, server):
    #assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    #msg['To'] = ", ".join(send_to)
    msg['To'] = COMMASPACE.join(send_to)
    #msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        #After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

# **** Edit parser.add_argument('emailServer DEFAULT value to your smtp server ****  
# **** This may be taken from a config file or predefined variable in the future or may not be needed ****
parser = argparse.ArgumentParser(description='SFTP Transfer Python script')
parser.add_argument('-files',
                    action='append',
                    dest='fileList',
                    metavar='"/path/to/file1" "/path/to/file2" <...>"',
                    required=False,
                    help='"/path/to/file1"')
parser.add_argument('-emailServer',
                    action='store',
                    dest='emailServer',
                    default='email.server.tld',
                    metavar='server.mail.com',
                    required=False,
                    help='email server')
parser.add_argument('-from',
                    action='store',
                    dest='fromAddr',
                    default=socket.gethostname() + "@localdomain",
                    metavar='"user@domain.com"',
                    required=False,
                    help='address to send from')
parser.add_argument('-to',
                    action='store',
                    nargs='+',
                    dest='toAddr',
                    metavar='"user@domain.com"',
                    required=True,
                    help='recipients of message')
parser.add_argument('-subject',
                    action='store',
                    dest='emailSubject',
                    metavar='"Subject text"',
                    required=False,
                    help='Subject text of email message')
parser.add_argument('-body',
                    action='store',
                    dest='emailBody',
                    metavar='"Body text"',
                    required=False,
                    help='Body text of email message')


args = parser.parse_args()

fileList = args.fileList
emailServer = args.emailServer
fromAddr = args.fromAddr
toAddr = args.toAddr
emailSubject = args.emailSubject
emailBody = args.emailBody


send_mail(fromAddr, toAddr, emailSubject, emailBody, fileList, emailServer)
