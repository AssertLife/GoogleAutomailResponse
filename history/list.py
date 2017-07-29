

"""

#startHistoryId (string) -  Required. Returns history records after the specified startHistoryId.
							The supplied startHistoryId should be obtained from the historyId of a message, thread, or previous list response.
							History IDs increase chronologically but are not contiguous with random gaps in between valid IDs.
							Supplying an invalid or out of date startHistoryId typically returns an HTTP 404 error code.
							A historyId is typically valid for at least a week, but in some rare circumstances may be valid for only a few hours.
							If you receive an HTTP 404 error response, your application should perform a full sync.
							If you receive no nextPageToken in the response, there are no updates to retrieve and you can store the returned historyId for a future request.

https://developers.google.com/gmail/api/v1/reference/users/history/list
"""
def ListHistory(service, user_id, historyTypes = '', labelId = '', startHistoryId='1'):

    history = service.users().history().list(userId=user_id,
                                             historyTypes=historyTypes,
                                             labelId=labelId,
                                             startHistoryId=startHistoryId).execute()
    print(startHistoryId)
    
    changes = history['history'] if 'history' in history else []
    while 'nextPageToken' in history:
        page_token = history['nextPageToken']
        history = service.users().history().list(userId=user_id,
                                        historyTypes=historyTypes,
                                        labelId=labelId,
                                        startHistoryId=startHistoryId,
                                        pageToken=page_token
                                        ).execute()
        changes.extend(history['history'])
    return changes
