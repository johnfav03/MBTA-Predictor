import smtplib
import pandas as pd
from datetime import datetime
carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def send(message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
	to_number_A = '2488789412{}'.format(carriers['verizon'])
	to_number_B = '9787276138{}'.format(carriers['verizon'])
	auth = ('tpredsms@gmail.com', 'znfnrsfofosyskvg')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])
	print(message)

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number_A, message)
	server.sendmail( auth[0], to_number_B, message)
	
scores = pd.read_csv('data/scores.csv')
total_mae = scores['mae'].mean()
daily_mae = scores['mae'].iloc[-1]
curr_time = datetime.now()
res = str(curr_time.strftime('[%m/%d] ')) + str(round(daily_mae, 2)) + ", " + str(round(total_mae, 2))
send(res)