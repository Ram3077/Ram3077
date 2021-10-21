from datetime import datetime, timedelta
import json
import httplib2
import os
from numpy.core import records
from numpy.core.fromnumeric import size
from numpy.core.shape_base import block
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
from collections import Counter
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
import threading, time
from tkinter import*

class deliverRecipientObject(object):
    def __init__(self):
         self.deliveryType = ""
         self.id = ""
         self.type = ""

   



class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, deliverRecipientObject):
            return {}
        return (MyJsonEncoder, self).dumps(obj)

# resp = requests.post('google.com')
# resp.content


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'C:\\Users\\sri\\Desktop\\glance\\client_secret_672560470766-r8jre2vneh1h8nch7qn0anldtrhh3j38.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials(user_email):
    # home_dir = '/home/selvaprakash/glance/'
    home_dir = 'C:\\Users\\sri\\Desktop\\glance'
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   user_email+'-gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, tools.argparser.parse_args(args=['--noauth_local_webserver']))
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
    else: 
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "me", message1)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_bytes())}

def createMessageWithAttachment(
    sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients          
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)


    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def main():
    to = "to@address.com"
    sender = "from@address.com"
    subject = "subject"
    msgHtml = "Hi<br/>Html Email"
    msgPlain = "Hi\nPlain Email"
    SendMessage(sender, to, subject, msgHtml, msgPlain)
    # Send message with attachment: 
    SendMessage(sender, to, subject, msgHtml, msgPlain, '/path/to/file.pdf')

def read_msg(user_email):
    credentials = get_credentials(user_email)

    service = build('gmail', 'v1',credentials=credentials)

    # request a list of all the messages
    result = service.users().messages().list(userId='me',maxResults=10).execute()
    print ('result ', result)
    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    contents = []
    dup=()
    date=()
    
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        #print (txt)
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']
            # print (payload)

            for d in headers:
                if d['name']=='Date':
                    date=d['value']
                    print(date)
                
                    


            
        
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
            print("From: ", sender)
            print("DATE: ", date)
            # print("Message: ", soup.decode_contents())
            # print('\n')
            info = {
        "sender":    sender,
        "date": date,
        }
            contents.append(info)
              

        except:

            pass
   
    df=pd.DataFrame(contents) 
    print('updated',df.columns)
    print('***********************')
    # df['date']=pd.to_datetime(df['date'])
    # df=df.set_index(['date'])
    # print(df)
    # print('selected_dates',df.loc['2021-09-20':'2021-10-01'])

    # print('modified',df)
    print('col names',df.columns)
    
    
    df['COUNT']=1    
    # print('new columns',df)
    # print(df.columns)


    df_sum=df.groupby('sender').size()
    # print('df_sum',df_sum)
    print('df sum columns',df_sum.to_frame())



    

    dup=df.pivot_table(index=("sender"),aggfunc='count')
    print(type(dup))
    print('d',dup)
   
    json = dup.reset_index().to_json(orient='index')
    email_list=json
    print('changes json',json)
   
    dup.reset_index().to_json('C:\\Users\\sri\\Desktop\\glance\\mailjsonformat.json',orient='records')
    print('saved json')

    dict=ast.literal_eval(json)
    dataFra=pd.DataFrame(data=(dict));
    

    
    plt.title('duplicate count in barh')
    plt.xlabel("sender_msg",fontsize=15)
    plt.ylabel("sender_count",fontsize=15)
    plt.barh(range(len(dict)),sorted(dict),color='blue',alpha=0.5)
    # # dup.sort_values("sender",ascending=False)
    plt.show(block=True)
   
    return (dup)
    

    

if __name__ == '__main__':
    read_msg('selva.prakash@gmail.com')