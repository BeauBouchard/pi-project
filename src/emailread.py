#!/usr/bin/env python3

import time
import datetime 
import imaplib 
import email
import sys
import os

#=====================EMAIL=====================
EMAIL_TO	= "youremail@gmail.com"
EMAIL_FROM	= "*email@email.com*"
PWD_FROM	= "Pass gose here"
SMTP_SERVER	= "imap.gmail.com"
SMTP_PORT	= 993
MAILBOX		= "INBOX"
#=====================EMAIL=====================


# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

# logs into an email with the characters listed above.

def login_to_email():
	try:
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		mail.login(EMAIL_FROM,PWD_FROM)
	except imaplib.IMAP.error:
		print("failed to login.")
	return mail

def delete_mail(mail):
	
	try:
		# Got the list of uids in my inbox:
		mail.select(MAILBOX)
		result, data = mail.uid('search', None, "ALL")
		uidList = data[0].split()
			
		#Delete the emails in the newUidList
		for uid in uidList:
			mail.uid("STORE",uid, '+X-GM-LABELS', '\\Trash')
		print("All mail moved to trash.")
			
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print("+=====================================================+")
		print("Error deleting mail.")
		print("+=====================================================+\r")		
		
# NOTE: dependent on def delete_email()
def process_mailbox(mail):
	try:
		rv, data = mail.search(None,"ALL") 
		qty = data[0].split()
		print("qty=",qty)
		if qty == []:
			time.sleep(10)
			return
		qty = int(qty[-1])
		print("%s messages found" %(qty))
		print("Getting messages")
		for i in data[0].split():
			rv, data = mail.fetch(i, '(RFC822)')
			if rv != 'OK':
				print("Error getting messages.")
				return
			
			msg = email.message_from_bytes(data[0][1])
			print('%s From: %s' %(i,msg['From']))
			print('%s Message: %s' %(i,msg['Subject']))
			print('Sent Data:', msg['Date'])
			date_tuple = email.utils.parsedate_tz(msg['Date'])
			if date_tuple:
				local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
				print("Local Date:" , local_date.strftime("%a, %d %b %Y %H:%M:%S"))
				print('----------------------------------------------\r')
			if msg['Subject'] == "Run_Program":
					delete_mail(mail)
					mail.close()
					mail.logout()
					os.system("python3 Run_Program.py")
					read_mailbox(MAILBOX)

				
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print("+=====================================================+")
		print("Error while processing mail.")
		print("+=====================================================+\r")
		return
			

# NOTE: Process dependent on def process_mailbox()
# NOTE: Process dependent on def login_to_email()
# Reads the content of a mailbox within the logged in email.
def read_mailbox(MAILBOX):
	try:
		#rv, mailboxes = mail.list()
		#if rv == "OK":
		#	print("Mailboxes:")
		#	print(mailboxes)
		mail = login_to_email()
			
		while True:
			rv, data = mail.select(MAILBOX) 		# rv is 'OK' , data raw content of mailbox
			if rv == 'OK':					# Check to see if mailbox was found.
				print("Processing mailbox...\n")	
				process_mailbox(mail)			# See def above.
				#mail.close()
			else:
				print("Can not find in-box.")
		mail.close()
		mail.logout()

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print("+===============================================================+")
		print("Error while reading email.")
		print("+===============================================================+ \r")
		 

read_mailbox(MAILBOX)


