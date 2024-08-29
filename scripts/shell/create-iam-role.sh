#!/bin/bash

aws iam create-role \
  --role-name AWSLambda-EmailSubmissionTemplate-Lambda-2 \
  --assume-role-policy-document file://$(pwd)/iam-role.json