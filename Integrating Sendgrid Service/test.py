import sendgrid
import os
from sendgrid.helpers.mail import *



sg = sendgrid.SendGridAPIClient('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')
from_email = From("pnt2022tmi14769@gmail.com")
to_email = To("pnt2022tmi14769@gmail.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)