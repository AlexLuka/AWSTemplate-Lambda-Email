#!/bin/bash

# The following environment variables are required
#   AWS_REGION
#   AWS_ACCOUNT_ID
#   SES_EMAIL
#   SES_VERIFIED_RECIPIENT

#
#
# First create IAM role and required polices
LAMBDA_FUNCTON_NAME=SendEmail
ROLE_NAME=AWSLambda-EmailSubmissionTemplate-Lambda
POLICY_NAME=AWSLambda-EmailSubmissionTemplate-SESAccessPolicy

aws iam create-role \
  --role-name ${ROLE_NAME} \
  --assume-role-policy-document file://$(pwd)/iam-role.json \
  --region ${AWS_REGION} \
  --no-paginate

# ARN will be "arn:aws:iam::***:policy/AWSLambda-EmailSubmissionTemplate-SESAccessPolicy"
aws iam create-policy \
  --policy-name ${POLICY_NAME} \
  --policy-document file://$(pwd)/ses-policy.json \
  --description "Policy that should allow Lambda to send emails using SES" \
  --region ${AWS_REGION} \
  --no-paginate

aws iam attach-role-policy \
  --role-name ${ROLE_NAME} \
  --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME} \
  --region ${AWS_REGION} \
  --no-paginate

#
# Next...
# Go to the location where sources are and create a zip archive
cd ../../src/email_lambda
zip -r ../../archives/email_lambda.zip ./*

#
# Then
# Go back to root of the repo
cd ../..
ZIP_FILE="fileb://$(pwd)/archives/email_lambda.zip"
echo $ZIP_FILE

#
# Finally,
# create a lambda function with corresponding name and role
# We need to sleep for 5 seconds because the role creation has some delay
# and lambda may not be created immediately, but delay fixes the issue.
sleep 5

aws lambda create-function                \
  --function-name ${LAMBDA_FUNCTON_NAME}  \
  --runtime python3.12                    \
  --handler main.run                      \
  --timeout 60                            \
  --architectures x86_64                  \
  --zip-file ${ZIP_FILE}                  \
  --no-paginate                           \
  --region ${AWS_REGION}                  \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME} \
  --environment "Variables={SES_EMAIL=${SES_EMAIL},SES_VERIFIED_RECIPIENT=${SES_VERIFIED_RECIPIENT}}"
