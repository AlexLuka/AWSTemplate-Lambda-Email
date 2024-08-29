#!/bin/bash

# Go to the location where sources are
cd ../../src/email_lambda
zip -r ../../archives/email_lambda.zip ./*

# Go back to root of the repo
cd ../..
ZIP_FILE="fileb://$(pwd)/archives/email_lambda.zip"
echo $ZIP_FILE

aws lambda create-function  \
  --function-name SendEmail \
  --runtime python3.12      \
  --handler main.run        \
  --timeout 60              \
  --architectures x86_64    \
  --zip-file ${ZIP_FILE}    \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/AWSLambda-EmailSubmissionTemplate-Lambda
