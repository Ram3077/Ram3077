from tkinter import getint
from flask import Flask,render_template,request,url_for,session
import writemail
import requests


app = Flask(__name__)
app.secret_key = '7gLgoG7a8ZgBuFRDRQQcD5qjZ0LrPF'


@app.route('/', methods=['GET', 'POST'])
def index():



    if request.method =='POST':
        user_email = request.form['email']
        print('State in App',request.args.get('state'),  session.get('_google_authlib_state_'))

        contents= writemail.read_msg(user_email)
        print (contents)

        return render_template('contents.html',data = contents)

    return render_template('email button.html')
    #return render_template('get_emails.html')


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
    code = request.args.get("code")
    print ('Returned Code',code)

    return render_template('get_emails.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('Blog.html')

@app.route('/About', methods=['GET'])
def about():
    return render_template('About.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()

 git init