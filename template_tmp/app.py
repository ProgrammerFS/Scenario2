from config import app, mail
from mailbox import Message

@app.route("/send_mail/", methods=['GET', 'POST'])
def index():
    email = "Scenario2group25@gmail.com"
    mail_message = Message(
            'Hi ! Don’t forget to follow me for more article!', sender=email, recipients=["andywu2513@gmail.com"])
    mail_message.body = "This is a test"
    mail.send(mail_message)
    return "Mail has sent"
if __name__ == '__main__':
   app.run(debug=True)

# from flask import Flask
# from flask_mail import Mail, Message

# app = Flask(__name__)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'Scenario2group25@gmail.com'
# app.config['MAIL_PASSWORD'] = 'zwco gwie ntlg jivy'
# mail = Mail(app)

# @app.route(r'/send_email')
# @app.route(r'/')
# def index():
#     msg = Message('Hello', recipients=['andywu2513@example.com'])
#     msg.body = 'This is a test email'
#     mail.send(msg, sender='Scenario2group25@gmail.com')
#     return 'Email sent'

# if __name__ == '__main__':
#     app.run(debug=True)