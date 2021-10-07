from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.file import Storage

from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from bs4 import BeautifulSoup




# Initialize the object for the Gmail API
# https://developers.google.com/gmail/api/quickstart/python
SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('client_secret.json')
creds = store.get()
# creds=''
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret_672560470766-b80mi80cgvg4sima878v5k88s6g18qr1.apps.googleusercontent.com.json', SCOPE)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


    # request a list of all the messages
result = service.users().messages().list(userId='me',maxResults=5).execute()

messages = result.get('messages')
contents = []

for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        # print (txt)
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']
            # print (payload)

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                    # print (subject)
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            # print (parts)
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
            # print (decoded_data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data)
            # print (soup)
            # body = soup.body()
            # print (body)
            body = soup.decode_contents()

            # Printing the subject, sender's email and message
            # print("Subject: ", subject)
            # print("From: ", sender)
            # print("Message: ", soup.decode_contents())
            # print('\n')
            info = {
        "sender":    sender,
        "subject": subject,
        "body":  body
        }
            contents.append(info)
        except:

            pass
