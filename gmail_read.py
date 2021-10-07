from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import flask
import os

# Define the SCOPES. If modifying it, delete the token.pickle file.
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='pagemail-319603-226fa0e6fc71.json'

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails(user_email,state):
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    # if os.path.exists('token'+user_email+'.pickle'):

    #     # Read the token from the file and store it in the variable creds
    #     with open('token'+user_email+'.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    #         print (creds)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret_672560470766-b80mi80cgvg4sima878v5k88s6g18qr1.apps.googleusercontent.com.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            flow.redirect_uri = 'https://www.glance.email/oauth2callback'
            authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
            flask.session['state'] = state

            print ('flask json' , flask.request.json)
            authorization_response = flask.request.url
            print ('auth_resp',authorization_response)
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            flask.session['credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}

        # Save the access token in token.pickle file for the next run
        # with open('token.pickle', 'wb') as token:
        #     pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1',credentials=credentials)

    # request a list of all the messages
    result = service.users().messages().list(userId='me',maxResults=5).execute()
    # print (result)
    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    contents = []

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
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
    return (contents )

# getEmails('selva.prakash@gmail.com')

#getEmails('selva.prakash@gmail.com')

