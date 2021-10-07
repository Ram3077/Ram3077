POST https://yourserver.example.com/yourUrl
Content-type: application/json

{
  message:
  {
    // This is the actual notification data, as base64url-encoded JSON.
    data: "eyJlbWFpbEFkZHJlc3MiOiAidXNlckBleGFtcGxlLmNvbSIsICJoaXN0b3J5SWQiOiAiMTIzNDU2Nzg5MCJ9",

    // This is a Cloud Pub/Sub message id, unrelated to Gmail messages.
    "messageId": "2070443601311540",

    // This is the publish time of the message.
    "publishTime": "2021-02-26T19:13:55.749Z",
  }

  subscription: "projects/myproject/subscriptions/mysubscription"
}