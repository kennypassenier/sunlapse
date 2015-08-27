#This is just a file I use as playground to test stuff.

with open('mail_creds.txt', 'r') as f:
    text_data = f.read()
sender = text_data.split('+')[0]
sender_pass = text_data.split('+')[1]
print(sender, sender_pass)
