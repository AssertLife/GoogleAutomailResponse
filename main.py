# [START app]
import base64
import json
import logging
import os
import email.header
import httplib2

import notifications.process
import watch.do
import oauth.credentials.get


from flask import current_app, Flask, render_template, request
from google.cloud import pubsub

from googleapiclient.discovery import build




app = Flask(__name__)
# Configure the following environment variables via app.yaml
# This is used in the push request handler to veirfy that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']


# Global list to storage messages received by this instance.
MESSAGES = []


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APP_ID = 'automailresponse-173812'
APP_NAME = 'AutomailResponse'
REDIRECT_URI = 'http://0.0.0.0/oauth2callback'


service = None
credentials = None
historyId = None


# [START index]
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', messages=MESSAGES)

    ps = pubsub.Client()
    topic = ps.topic(current_app.config['PUBSUB_TOPIC'])

    topic.publish(
        request.form.get('payload', 'Example payload').encode('utf-8'))

    return 'OK', 200
# [END index]


# [START push]
@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    if(request.args.get('token', '') != current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    global historyId
    envelope = json.loads(request.data.decode('utf-8'))
    historyId = notifications.process.ProcessNotification(service, envelope, historyId) # XXX startHistoryId

    MESSAGES.append(envelope)


    # Returning any 2xx status indicates successful receipt of the message.
    return 'OK', 200
# [END push]

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500



@app.before_first_request
def initialize_service():
    global service, credentials, historyId

    credentials = oauth.credentials.get.GetCredentials(SCOPES, CLIENT_SECRET_FILE, REDIRECT_URI, APP_NAME)
    http = credentials.authorize(httplib2.Http())
    service = build('gmail', 'v1', http=http)

    historyId = watch.do.WatchChanges(service, 'me', APP_ID, app.config['PUBSUB_TOPIC'])


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]




