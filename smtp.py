import smtplib

sender = "preetrajgupta2002@gmail.com"
receiver = "preetrajgupta2002@gmail.com"
password = "Your Password"

port_no = 587
smtp_url = "smtp.gmail.com"

mail = smtplib.SMTP(smtp_url, 587)
mail.ehlo()
mail.starttls()
mail.login(sender, password)

rain = True
humidity = 123
temperature = 123

header = "To: " + str(receiver) + "\nSubject: Weather Alert !!! by Smart Station\n"
content = "Hey there!\nI guess you gotta romance with your umbrella today\n"

if rain:
    content += "Rain: " + str(rain) + "\n"
else:
    content += "The weather stays clear and sound\n"

content += "Humidity: " + str(humidity) + "\n"
content += "Temperature: " + str(temperature) + " C\n"
content += "Distance from Ground: ...\n"

message = header + content
print(message)
mail.sendmail(sender, receiver, message)
mail.close()
