from flask import Flask,render_template,request
import sub
import requests
import pandas as pd
from inspect import currentframe
import json

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_line


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'GET':
    #     sender, subject,body = getEmails()
    #     print ('Sender: ',  sender)
    #     print ('Subject: ', subject)
    #     print ('Body: ',body)

    if request.method =='POST':
        user_email = request.form['email']
        contents= sub.read_msg(user_email)
        #print (contents)
        print (type(contents))
        cont_df = pd.DataFrame(contents)
        # print (contents[0]['sender'])
        cont_df=cont_df.reset_index()
        # print(contents['subject'])
        print (cont_df.columns," -- Line Number")
        print(cont_df.subject.to_string(index=False))
        print (cont_df.sender.to_string(index=False))
        print (cont_df.groupby(by=["sender"]).count())
        cont_df_sender_count = cont_df.groupby(by=["sender"]).count()
        print (type(cont_df_sender_count))
        print (type(cont_df_sender_count.reset_index()))
        
        dup=pd.pivot_table(cont_df,index=('sender','date','subject'))
        print(type(dup))
        print('d',dup)
        print (dup.reset_index().to_json())
        cont_df_sender_count_json = dup.reset_index().to_json()
        print('***********************************************************************************')
        print ((dup.reset_index().to_dict(orient='records')))
        # return 0
        # return render_template('contents.html',data = contents)
        return render_template('chart.html',data = json.dumps(dup.reset_index().to_dict(orient='records')))

    return render_template('get_emails.html')






if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()