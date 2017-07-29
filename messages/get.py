# mformat (string) - The format to return the message in. (full/metadata/minimal/raw)
# mmetadataHeaders (string) - When given and format is METADATA, only include headers specified.
# https://developers.google.com/gmail/api/v1/reference/users/messages/get
def GetMessage(
	service, user_id, mid,
	mformat='full', mmetadataHeaders=''):
    return service.users().messages().get(userId=user_id, id=mid, format=mformat, metadataHeaders=mmetadataHeaders).execute()