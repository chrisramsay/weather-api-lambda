# weather-api-lambda
Somewhere to store lambda (λ) functions I use in AWS for my weather data API

## Updating lambda code

First add the updated `main.py` to the `lambda.zip` file:

```
raz@fromage:~/$ zip lambda.zip main.py
```

Now push the updated lambda package to S3:

```
raz@fromage:~/$ aws s3 cp lambda.zip s3://chrisramsay-lambdas
```

Finally, update the lambda code with the new zip contents in S3:

```
raz@fromage:~/$ aws lambda update-function-code --function-name getLatestNetSpeed --s3-bucket chrisramsay-lambdas --s3-key lambdas.zip

```