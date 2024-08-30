import os
import boto3

from botocore.exceptions import ClientError


"""
This code is based on an example found here:
    https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html
"""


AWS_REGION = "us-east-1"
CHARSET = "UTF-8"


def run(*args, **kwargs):
    print(f"Successfully executed lambda function with:")
    print(f"args={args}")
    print(f"Got {len(args)} input arguments")
    print(f"kwargs={kwargs}")

    client = boto3.client('ses', region_name=AWS_REGION)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    sender = f"Alexey Lukyanov <{os.environ.get('SES_EMAIL')}>"

    # This address must be verified until the account is in the sandbox
    recipient = os.environ.get('SES_VERIFIED_RECIPIENT')

    print(f"Environment:")
    print(f"sender={sender}")
    print(f"recipient={recipient}")

    # The subject line for the email.
    subject = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    body_text = (
        "Amazon SES Test (Python)\r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto).")

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
    """

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
