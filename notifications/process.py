import json
import base64
import email

import messages.get
import messages.send
import history.list
import mime.create

def ProcessNotification(service,
	envelope,
	startHistoryId):
    payload = base64.b64decode(envelope['message']['data'])
    mdata = json.loads(payload)

    hlist = history.list.ListHistory(service, mdata['emailAddress'],
                                     historyTypes='messageAdded',
                                     labelId='UNREAD',
                                     startHistoryId=startHistoryId)

    for h in hlist:
        print(h)
    	for madd in h['messagesAdded']:
            message = messages.get.GetMessage(service, mdata['emailAddress'], madd['message']['id'], mformat='raw')
            mime_msg = email.message_from_string(base64.urlsafe_b64decode(message['raw'].encode('ASCII')))
            
            if mdata['emailAddress'] in mime_msg['From']:
                print("invalid")
                print(mime_msg['From'])
                continue

    	    subject = 'Thank you for contacting me!'
    	    body = ''

    	    with open('mimemessage.html', 'r') as mmhtmlfile:
                body = mmhtmlfile.read()

    	    mmhtml = mime.create.CreateMIMEMessageHtml(
    			mdata['emailAddress'],
    			mime_msg['From'],
    			subject,
    			body)
    	    
    	    ret = messages.send.SendMessage(service, mdata['emailAddress'], {'raw': base64.urlsafe_b64encode(mmhtml.as_string())})
    	    if ret is None:
                print(ret)

    return mdata['historyId']
