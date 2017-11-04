import argparse
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

# Parse the project name
parser = argparse.ArgumentParser()
parser.add_argument(
    '--days', default=30, type=int,
    help='Clean up AMI images older than X days (default = 30 days)',
)
parser.add_argument(
    '--region', default='us-west-2', type=str,
    help='AWS region to watch for AMIs (default = us-west-2)',
)
parser.add_argument(
    '--owner', default='123456789012', type=str,
    help='AWS account owner ID (default account number is fictional)',
)
# Get the timeout from config
args = parser.parse_args()
days_count = args.days
aws_region = args.region
account_owner_image_id = args.owner
ami_age_limit = datetime.now() - timedelta(days=days_count)

ec2_client = boto3.client('ec2', region_name=aws_region)

images_list = ec2_client.describe_images(Owners=[account_owner_image_id])
cleanup_counter = 0
for image in images_list['Images']:
    image_id = image['ImageId']
    date_string = image['CreationDate']
    image_dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    if image_dt < ami_age_limit:
        instances_list = ec2_client.describe_instances(
            Filters=[{'Name': 'image-id', 'Values': [image_id]}]
        )
        active_reservations = instances_list['Reservations']
        if not active_reservations:
            # There might be a client error if we run int multiple times
            try:
                ec2_client.deregister_image(ImageId=image_id)
            except ClientError:
                pass
            print('Image %s is removed' % image_id)
            cleanup_counter += 1

if cleanup_counter:
    print('Totally %s images have been cleaned up.' % cleanup_counter)
else:
    print('There is no images to be removed.')
