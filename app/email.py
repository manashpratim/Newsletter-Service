from datetime import datetime

from azure.communication.email import EmailClient

from app.core.config import settings
from app.utils.exceptions.common_exceptions import ProcessError


def send_newsletter_email(
    recipient_email: str,
    subscriber_name: str,
    subject: str,
    body_text: str,
    body_html: str | None = None,
):
    """
    Sends a newsletter email to a subscriber using Azure Communication Services.
    Raises ProcessError if sending fails.
    """

    try:
        connection_string = settings.EMAIL_CONNECTION_STRING
        client = EmailClient.from_connection_string(connection_string)

        sender_email = "DoNotReply@loong.co.in"

        # If no HTML provided, build a default newsletter-themed HTML layout
        if body_html is None:
            body_html = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            max-width: 650px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background-color: #0078D4;
            padding: 18px;
            color: #ffffff;
            text-align: center;
        }}
        .content {{
            padding: 25px;
            line-height: 1.6;
        }}
        .footer {{
            background-color: #f0f0f0;
            padding: 10px;
            font-size: 12px;
            text-align: center;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>{subject}</h2>
        </div>
        <div class="content">
            <p>Hi {subscriber_name},</p>
            <p>{body_text}</p>
        </div>
        <div class="footer">
            <p>You are receiving this newsletter because you subscribed to our service.</p>
            <p>&copy; {datetime.now().year} Newsletter Service. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

        message = {
            "senderAddress": sender_email,
            "recipients": {"to": [{"address": recipient_email}]},
            "content": {
                "subject": subject,
                "plainText": body_text,
                "html": body_html,
            },
        }

        # Send the email and wait for completion
        poller = client.begin_send(message)
        result = poller.result()

    except Exception as error:
        raise ProcessError(f"Failed to send newsletter to {recipient_email}: {error}")

    # Azure result validation
    status = result.get("status")

    if status is None:
        # some ACS clients don't include a status → treat as success
        return

    if str(status).lower() != "succeeded":
        raise ProcessError(f"Newsletter send failed for {recipient_email}: {result}")
