from dotenv import load_dotenv
import os
import imaplib

# Load environment variables from .env file
load_dotenv()

# IMAP settings
username = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
imap_server = "mail.meulindo.fun"
imap_port = 992

def mailLogin():
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    return imap