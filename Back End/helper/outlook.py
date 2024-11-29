import requests
import json
import base64
import datetime
class OutlookEmailSender:
    def __init__(self, access_token):
        self.access_token = access_token
        self.graph_url = 'https://graph.microsoft.com/v1.0'

    def send_email(self, subject, body, to_recipients, attachments=None):
        email_msg = {
            'Message': {
                'Subject': subject,
                'Body': {
                    'ContentType': 'Text',
                    'Content': body
                },
                'ToRecipients': [{'EmailAddress': {'Address': recipient}} for recipient in to_recipients],
                'Attachments': []
            },
            'SaveToSentItems': 'true'
        }

        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as file:
                    content_bytes = file.read()
                    content_base64 = base64.b64encode(content_bytes).decode()
                    email_msg['Message']['Attachments'].append({
                        '@odata.type': '#microsoft.graph.fileAttachment',
                        'Name': attachment.split('/')[-1],
                        'ContentBytes': content_base64
                    })

        # Instead of sending the email, return a redirect link
        redirect_link = f"https://outlook.office.com/mail/deeplink/compose?subject={subject}&body={body}&to={','.join(to_recipients)}"
        print(f'Redirect link: {redirect_link}')
        return redirect_link

# Example usage:
# access_token = 'YOUR_ACCESS_TOKEN'
# email_sender = OutlookEmailSender(access_token)
# email_sender.send_email('Test Subject', 'Test Body', ['recipient@example.com'], ['path/to/attachment1', 'path/to/attachment2'])
    def fetch_emails(self):
        url = f'{self.graph_url}/me/mailFolders/inbox/messages'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            '$filter': f'receivedDateTime ge {datetime.datetime.now() - datetime.timedelta(days=14)}',
            '$orderby': 'receivedDateTime DESC'
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            emails = response.json().get('value', [])
            for email in emails:
                print(f"Subject: {email['subject']}, Received: {email['receivedDateTime']}")
        else:
            print(f'Error fetching emails: {response.status_code}')
            print(response.json())

# Example usage:
# access_token = 'YOUR_ACCESS_TOKEN'
# email_sender = OutlookEmailSender(access_token)
# email_sender.fetch_emails()