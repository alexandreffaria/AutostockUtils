from mailLogin import mailLogin
from grabTopEmail import grabTopEmails

imap = mailLogin()
topEmails = grabTopEmails(imap, 3)
print(topEmails)
# close the connection and logout
imap.close()
imap.logout()
