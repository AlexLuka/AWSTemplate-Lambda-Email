#!/bin/bash

aws iam create-role \
  --role-name AWSLambda-EmailSubmissionTemplate-Lambda \
  --assume-role-policy-document file://$(pwd)/iam-role.json