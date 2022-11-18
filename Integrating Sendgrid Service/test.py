import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='pnt2022tmi14769@gmail.com',
    to_emails='gkvv2303@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(api_key='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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
