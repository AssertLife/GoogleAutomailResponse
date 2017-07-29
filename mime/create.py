from email.mime.text import MIMEText

"""
# sender (string) - the sender's email address
# to (string) - the receiver's email address
# subject (string) - the email's subject
# body (string) - email content (... aka body)
"""
def CreateMIMEMessageHtml(
	sender, to,
	subject, body):
	msg = MIMEText(body, 'html')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = to

	return msg