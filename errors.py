from apiclient import errors
# ...

def ListMessages(service, user, query=''):
  """Gets a list of messages.

  Args:
    service: Authorized Gmail API service instance.
    user: The email address of the account.
    query: String used to filter messages returned.
           Eg.- 'label:UNREAD' for unread Messages only.

  Returns:
    List of messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user, q=query).execute()
    messages = response['messages']

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)
    if error.resp.status == 401:
      # Credentials have been revoked.
      # TODO: Redirect the user to the authorization URL.
      raise NotImplementedError()