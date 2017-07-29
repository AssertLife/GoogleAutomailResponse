"""
body (string) - Request body
In the request body, supply a Users.messages resource with the following properties as the metadata. For more information, see the document on media upload.

https://developers.google.com/gmail/api/v1/reference/users/messages/send
"""
def SendMessage(
	service,
	user_id,
	mbody):
	return service.users().messages().send(userId=user_id, body=mbody).execute()