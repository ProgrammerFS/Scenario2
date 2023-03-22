from flask import Flask
from flask_mail import Mail
from mailbox import Message
import os
from dotenv import load_dotenv

load_dotenv()
os.getenv('/test/.env')

app = Flask(__name__)
app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('Scenario2group25@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('zwco gwie ntlg jivy')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)