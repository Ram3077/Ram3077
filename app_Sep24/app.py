from flask import Flask,render_template,request
import writemail
import requests


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
        contents= writemail.read_msg(user_email)
        print (contents)
        return render_template('contents.html',data = contents)

    return render_template('get_emails.html')






if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()