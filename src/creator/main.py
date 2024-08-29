import sys
import json
import boto3
import logging

from dotenv import load_dotenv


ROLE_NAME = "AWSLambda-EmailSubmissionTemplate-Lambda-2"


def init_logger(source, level=logging.DEBUG):
    logger_ = logging.getLogger(source)
    logger_.setLevel(level)

    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(level)

    logger_formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    logger_handler.setFormatter(logger_formatter)

    logger_.addHandler(logger_handler)
    return logger_


def create_role():
    role_policy = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    )

    client = boto3.client('iam')

    try:
        response = client.create_role(
            Path='/',
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=role_policy,
            Description="Role policy for Lambda execution",
            MaxSessionDuration=3600,
            Tags=[
                {
                    'Key': 'App',
                    'Value': 'EmailSend'
                },
            ]
        )
    except BaseException as e:
        if str(e) == ("An error occurred (EntityAlreadyExists) when calling the CreateRole operation: "
                      "Role with name AWSLambda-EmailSubmissionTemplate-Lambda-2 already exists."):
            print(f"Role already exists")
        else:
            print(f"Unknown error")
            return False

    # Response example:
    # {
    #   'Role': {
    #       'Path': '/',
    #       'RoleName': 'AWSLambda-EmailSubmissionTemplate-Lambda-2',
    #       'RoleId': 'AROAVRUVTZAOBP4VFCCPO',
    #       'Arn': 'arn:aws:iam::***:role/AWSLambda-EmailSubmissionTemplate-Lambda-2',
    #       'CreateDate': datetime.datetime(2024, 8, 29, 16, 37, 14, tzinfo=tzutc()),
    #       'AssumeRolePolicyDocument': {
    #           'Version': '2012-10-17',
    #           'Statement': [
    #               {
    #                   'Effect': 'Allow',
    #                   'Principal': {
    #                       'Service': 'lambda.amazonaws.com'
    #                   },
    #                   'Action': 'sts:AssumeRole'
    #               }
    #           ]
    #       },
    #       'Tags': [{'Key': 'App', 'Value': 'EmailSend'}]
    #   },
    #   'ResponseMetadata': {
    #       'RequestId': 'c04255fb-35b5-4b6d-9d72-edff45363b4d',
    #       'HTTPStatusCode': 200,
    #       'HTTPHeaders': {
    #       'date': 'Thu, 29 Aug 2024 16:37:13 GMT',
    #       'x-amzn-requestid': 'c04255fb-35b5-4b6d-9d72-edff45363b4d',
    #       'content-type': 'text/xml',
    #       'content-length': '960'
    #   },
    #   'RetryAttempts': 0}
    # }

    # print(response)
    return True


def main():
    role_creation_status = create_role()
    if not role_creation_status:
        logger.info("Stopping process of Lambda creation")
        return


if __name__ == "__main__":
    load_dotenv()
    logger = init_logger(__name__)

    main()
