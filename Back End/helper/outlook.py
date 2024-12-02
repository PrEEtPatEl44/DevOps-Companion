import requests
import json
import base64
import datetime
import urllib.parse
class OutlookEmailSender:
    def __init__(self, access_token):
        self.access_token = access_token
        self.graph_url = 'https://graph.microsoft.com/v1.0'

    def send_mail(self, subject, body, to_recipients, attachments=None):
        """
        Create a draft email with optional attachments and return a redirect link to the draft.
        """
        url = f'{self.graph_url}/me/messages'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Construct the email message
        email_msg = {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in to_recipients],
            "attachments": []
        }

        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    content_bytes = file.read()
                    content_base64 = base64.b64encode(content_bytes).decode()
                    email_msg["attachments"].append({
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": attachment.split("/")[-1],
                        "contentBytes": content_base64
                    })

        # Make the POST request to create a draft
        response = requests.post(url, headers=headers, json=email_msg)

        if response.status_code == 201:  # Created
            draft = response.json()
            draft_id = draft.get('id')
            if draft_id:
                redirect_link = f"https://outlook.office.com/mail/deeplink/compose/id/{draft_id}"
                print("Draft email created successfully!")
                print(f"Redirect link to draft: {redirect_link}")
                return redirect_link
            else:
                print("Draft created but no ID returned.")
                return None
        else:
            print(f"Error creating draft: {response.status_code} - {response.text}")
            return None


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

    def book_meeting(self, subject, start_time, end_time, attendees, location=None, body=None):
        """
        Book a meeting using Microsoft Graph API.
        """
        url = f'{self.graph_url}/me/events'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Construct the meeting details
        event = {
            "subject": subject,
            "start": {
                "dateTime": start_time,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "UTC"
            },
            "attendees": [
                {
                    "emailAddress": {"address": attendee, "name": attendee.split('@')[0]},
                    "type": "required"
                } for attendee in attendees
            ],
            "location": {
                "displayName": location or "Online Meeting"
            },
            "body": {
                "contentType": "Text",
                "content": body or "Please join the meeting."
            }
        }

        # Make the POST request to book the meeting
        response = requests.post(url, headers=headers, json=event)

        if response.status_code == 201:  # Created
            meeting = response.json()
            print("Meeting booked successfully!")
            print(f"Meeting ID: {meeting.get('id')}")
            return meeting
        else:
            print(f"Error booking meeting: {response.status_code} - {response.text}")
