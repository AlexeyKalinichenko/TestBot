print('Test bot!!')

import telebot
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import shelve
import credentials

bot = telebot.TeleBot(credentials.token)

@bot.message_handler(content_types = ['text'])
def GetMessage(message):
	if IsContentProhibited(message.text):
		counter = IncreaseCounter()
		SendEmail(message.text, counter)

def IsContentProhibited(message):
	result = False
	for word in credentials.nWords:
		index = message.find(word)
		if index != -1:
			result = True
			break
	return result

def IncreaseCounter():
	counter = 1
	with shelve.open("data") as state:
		key = 'counter'
		if key in state:
			counter = state[key] + 1
		state[key] = counter
	return counter

def SendEmail(source, counter):
	text = credentials.body
	text = text.replace('[source]', source)
	text = text.replace('[counter]', '{}'.format(counter))

	smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	smtp_server.login(credentials.sender, credentials.password)

	message = MIMEText(text, 'plain', 'utf-8')
	message['Subject'] = Header(credentials.subject, 'utf-8')

	smtp_server.sendmail(credentials.sender, credentials.recipient, message.as_string())
	smtp_server.close()

	print("*** Counter: {} ***".format(counter))

bot.polling(none_stop = True, interval = 0)
