import smtplib
import socket

def send_email(to, subject, text):
            gmail_user = "kennypybot@gmail.com"
            gmail_pwd = "kabelzalm"
            FROM = 'kennypybot@gmail.com'
            TO = [str(to)] #must be a list
            SUBJECT = str(subject)
            TEXT = str(text)

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER)
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print('successfully sent the mail')
            except:
                print("failed to send mail")
test = str(socket.gethostbyname(socket.gethostname()))
send_email("mendax1@gmail.com", "jow", test)
