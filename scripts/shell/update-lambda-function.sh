#!/bin/bash


LAMBDA_FUNCTON_NAME=SendEmail

aws lambda update-function-configuration  \
  --function-name ${LAMBDA_FUNCTON_NAME}  \
  --no-paginate                           \
  --environment "Variables={SES_EMAIL=${SES_EMAIL},SES_VERIFIED_RECIPIENT=${SES_VERIFIED_RECIPIENT}}"
