# Description

1. I had to create an execution role for my Lambda function on AWS.
   That parameter is required if create lambda function for the first time using CLI.
2. To create a lambda function, go to scripts/shell and run
   ```shell
   dotenv -e ../../.env -- ./create-lambda-function.sh
   ```