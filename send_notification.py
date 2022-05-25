import smtplib

# help(smtplib)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

smtpObj.starttls()

smtpObj.login('sensor.project.aga@gmail.com','2051868Dd')

smtpObj.sendmail("sensor.project.aga@gmail.com","agaton615@gmail.com","first check test")

smtpObj.quit()
