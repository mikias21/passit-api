import os
from mailjet_rest import Client

def send_email(subject: str, email: str, message: str):
    client = Client(auth=(os.getenv('MAILJET_API_KEY'), os.getenv('MAILJET_SECRET_KEY')), version='v3.1')
    data = {
        'Messages': [
            {
            "From": {
                "Email": "noreply@passit.com",
                "Name": "passit.io"
            },
            "To": [
                {
                "Email": email,
                "Name": email
                }
            ],
            "Subject": subject,
            "TextPart": "",
            "HTMLPart": message,
            "CustomID": "passit.io email"
            }
        ]
    }
    result = client.send.create(data=data)
    return result.status_code
