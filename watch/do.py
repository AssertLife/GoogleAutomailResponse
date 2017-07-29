def WatchChanges(
	service, user_id,
	project_id,
	topic_name):
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/{0}/topics/{1}'.format(project_id, topic_name)
    }

    hreturn = service.users().watch(userId=user_id, body=request).execute()
    return hreturn['historyId']