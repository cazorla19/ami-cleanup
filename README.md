# ami_cleanup

## What does this script do?

Clean up AMI images older than X days in AWS region Y. This script is searching through the instances trying to find one with old image. If nothing is found - the image will be removed.

## What should I have to run this script?

* Python 2.x/3.x
* boto3 module installed
* Necessary EC2 permissions for your AWS user

## Install dependencies

`pip install -r requirements.txt`

## How can I run this?

`python cleanup.py --days=30 --region=us-east-1`

If you want to change account - change owner ID

`python cleanup.py --days=90 --region=eu-west-1 --owner=123456789012`

## All available options

```
cazorla19$ python cleanup.py --help
usage: cleanup.py [-h] [--days DAYS] [--region REGION] [--owner OWNER]

optional arguments:
  -h, --help       show this help message and exit
  --days DAYS      Clean up AMI images older than X days (default = 30 days)
  --region REGION  AWS region to watch for AMIs (default = us-west-2)
  --owner OWNER    AWS account owner ID (default account number is fictional)
```
