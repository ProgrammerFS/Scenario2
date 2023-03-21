import smtplib
import os
import imghdr
from email.message import EmailMessage

# zwco gwie ntlg jivy

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['andywu2513@gmail.com', 'andywu2003913@gmail.com']

message = EmailMessage()
message['Subject'] = 'Check out these fruits'
message['From'] = EMAIL_ADDRESS
message['To'] = contacts

message.set_content('Lots of fruits')

message.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Fruits!</h1>
    </body>
</html>
""", subtype='html')


files = ['apple.jpg', 'banana.jpeg', 'orange.jpeg']

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name) # Determine what type of image we are attaching
        file_name = f.name

    message.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    # message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name) # For pdf files


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

    smtp.login('Scenario2group25@gmail.com', 'zwco gwie ntlg jivy')

    smtp.send_message(message)



# sender_email = "andywu2525@gmail.com"
# rec_email = "andywu2513@gmail.com"
# password = input(str("Please enter your password : "))
# message = "Hey, this was sent using python"

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(sender_email, password)
# print("Login success")
# server.sendmail(sender_email, rec_email, message)
# print("Email has been sent to ", rec_email)





