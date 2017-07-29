#!/usr/bin/python
# -*- coding: utf-8 -*-
from oauth2client.file import Storage
from oauth2client import client


def GetCredentials(
    SCOPES,
    CLIENT_SECRET_FILE,
    REDIRECT_URI,
    APPLICATION_NAME,
    ):

    credential_path = APPLICATION_NAME + '.json'

    print credential_path

    store = Storage(credential_path)
    credentials = store.get()

    print credentials

    if not credentials or credentials.invalid:

        # Step1 : Configure the client object

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE,
                scope=SCOPES, redirect_uri=REDIRECT_URI)
        flow.params['access_type'] = 'offline'  # offline access
        flow.params['include_granted_scopes'] = True  # incremental auth

        # Step 2: Redirect to Google's OAuth 2.0 Server

        auth_uri = flow.step1_get_authorize_url()

        # Step 3: Google prompts user for consent..... (takes part in the browser...)

        # Step 4: Handle the OAuth 2.0 server response
        # Done in Flask.....

    return credentials
