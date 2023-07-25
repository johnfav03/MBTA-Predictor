import smtplib
import pandas as pd
carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def send(message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
	to_number = '2488789412{}'.format(carriers['verizon'])
	auth = ('johnfav03@gmail.com', 'oqkklhetmrhvmerl')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])
	print(message)

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number, message)
	
scores = pd.read_csv('data/scores.csv')
total_rmse = scores['rmse'].mean()
total_mae = scores['mae'].mean()
daily_rmse = scores['rmse'].iloc[-1]
daily_mae = scores['mae'].iloc[-1]
res = "Daily >> [" + str(daily_mae) + ", " + str(daily_rmse) + "]\nTotal >> [" + str(round(total_mae, 2)) + ", " + str(round(total_rmse, 2)) + "]"
send(res)