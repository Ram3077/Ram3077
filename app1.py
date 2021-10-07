import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    return render_template('get_emails.html')

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret_672560470766-b80mi80cgvg4sima878v5k88s6g18qr1.apps.googleusercontent.com.json',
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
)

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = 'https://www.glance.email/oauth2callback'

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
print (authorization_url)

# return flask.redirect(authorization_url)

