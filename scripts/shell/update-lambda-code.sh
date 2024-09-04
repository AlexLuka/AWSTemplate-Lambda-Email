#!/bin/bash

LAMBDA_FUNCTON_NAME=SendEmail

#
# Next...
# Go to the location where sources are and create a zip archive
cd ../../src/email_lambda
cp ../../images/* .
zip -r ../../archives/email_lambda.zip ./*

rm *.jpg

#
# Then
# Go back to root of the repo
cd ../..
ZIP_FILE="fileb://$(pwd)/archives/email_lambda.zip"
echo $ZIP_FILE

aws lambda update-function-code           \
  --function-name  ${LAMBDA_FUNCTON_NAME} \
  --no-paginate                           \
  --zip-file ${ZIP_FILE}
